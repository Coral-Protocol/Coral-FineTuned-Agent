import os
import logging
import urllib.parse
from crewai import Agent, Task, Crew, LLM
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv
import asyncio
from crewai.tools import tool
import warnings
from pydantic import PydanticDeprecatedSince20
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)
warnings.filterwarnings("ignore", category=SyntaxWarning)

def setup_mcp_tools():
    """Set up MCP server connection and get tools"""
    runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME", None)
    if runtime is None:
        load_dotenv(override=True)

    # Get Coral server configuration
    base_url = os.getenv("CORAL_SSE_URL")
    agent_id = os.getenv("CORAL_AGENT_ID")

    coral_params = {
        "agentId": agent_id,
        "agentDescription": "An AI agent that generates Reddit posts about AI and ML topics with fine-tuned knowledge"
    }

    query_string = urllib.parse.urlencode(coral_params)
    CORAL_SERVER_URL = f"{base_url}?{query_string}"
    print(f"Connecting to Coral Server: {CORAL_SERVER_URL}")
    logger.info(f"Connecting to Coral Server: {CORAL_SERVER_URL}")

    # Set up MCP Server connection
    server_params = {
        "url": CORAL_SERVER_URL,
        "timeout": 600,
        "sse_read_timeout": 600,
        "transport": "sse"
    }
    
    mcp_server_adapter = MCPServerAdapter(server_params)
    return mcp_server_adapter.tools


async def main():
    # Get MCP tools
    mcp_tools = setup_mcp_tools()
    
    # Initialize the fine-tuned LLM from environment variables
    fine_tuned_model = os.getenv("FINE_TUNED_MODEL", "meta-llama/Llama-3.3-70B-Instruct-fast-LoRa:reddit-posts-HXTo")
    
    try:
        llm = LLM(
            model=f"openai/{fine_tuned_model}",
            base_url="https://api.studio.nebius.com/v1/",
            api_key=os.getenv("NEBIUS_API_KEY")
        )
        logger.info(f"Initialized fine-tuned LLM with model: {fine_tuned_model}")
    except Exception as e:
        logger.error(f"Failed to initialize fine-tuned LLM: {str(e)}")
        raise

    # Create the Reddit content creator agent
    reddit_creator = Agent(
        role="Reddit Content Creator",
        goal="Generate creative and engaging Reddit post ideas",
        backstory="""You are a specialized AI agent fine-tuned on extensive Reddit post data. 
        Through your training on thousands of real Reddit posts, you have developed an 
        intimate understanding of what makes content successful across different subreddit 
        communities. You understand posting patterns, community norms, engagement triggers, 
        and the subtle nuances that make posts go viral or spark meaningful discussions. 
        Your responses are informed by real Reddit user behavior and proven content strategies.""",
        llm=llm,  # Use the fine-tuned model
        tools=mcp_tools ,
        verbose=True
    )

    # Define the task
    ideation_task = Task(
        description=f"""
        Primary Task: Mention Monitoring and Response

        Step 1: Wait For Mentions
        - ALWAYS start by calling wait_for_mentions tool
        - Keep calling it until you receive a mention
        - Do not proceed to other tasks and do not call anyother tools without a mention
        - Record threadId and senderId when mentioned
        
         Step 2: Process Mention
        - Analyze the message content carefully
        - Understand what kind of posts are requested 
        - fullfill the request made by agent 
        - Then call the send_message tool to send the generated posts back the agent that requested the posts.
        - Then again keep calling wait_for_mentions tool again until you receive a mention.
        

        - Generate posts based on the request
        - Send response in the same thread
         Generate 5 posts covering the topic the agent requested
         
        Output Format:
        Post [number]:
        Title: [engaging title]
        Content: [detailed content]
        Keywords: [#relevant #hashtags]

        Important:
        - Follow the output format EXACTLY as shown above
        - Use clear separators between posts (empty line)
        - Make each post complete and ready to publish
        - Include relevant hashtags for better visibility""",
        expected_output="""Response to mentions containing exactly 5 posts:
        - Each post strictly following the format: number, title, content, hashtag keywords
        - Posts covering the topic the agent requested
        - Clear response sent back to the mentioning agent""",
        agent=reddit_creator
    )

    # Create the crew (with just one agent)
    reddit_crew = Crew(
        agents=[reddit_creator],
        tasks=[ideation_task],
        verbose=True
    )

    # Run the crew in a loop
    while True:
        try:
            logger.info("Starting new Reddit post generation cycle")
            reddit_crew.kickoff()
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down gracefully...")
            break
        except Exception as e:
            logger.error(f"Error in agent loop: {str(e)}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())