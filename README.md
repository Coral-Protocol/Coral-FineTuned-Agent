## [Fine-Tuned Agent](https://github.com/Coral-Protocol/Coral-FineTuned-Agent)
 
AI Content Generation Agent powered by custom fine-tuned language models for specialized Reddit post creation. This agent leverages fine-tuned LLMs trained on specific datasets to generate highly targeted and domain-specific content with superior understanding of community norms and engagement patterns.

## Responsibility
Fine-Tuned Agent serves as a Reddit Content Creator that generates creative and engaging Reddit post ideas using custom fine-tuned language models. Through training on extensive Reddit post datasets, the agent has developed an intimate understanding of what makes content successful across different subreddit communities. It understands posting patterns, community norms, engagement triggers, and the subtle nuances that make posts go viral or spark meaningful discussions. The agent's responses are informed by real Reddit user behavior and proven content strategies embedded through the fine-tuning process.

## Details
- **Framework**: CrewAI
- **Tools used**: Coral MCP Tools
- **AI model**: Custom Fine-Tuned Models (via Nebius AI Studio)
- **Default Model**: meta-llama/Llama-3.3-70B-Instruct-fast-LoRa
- **Date added**: September 12, 2025
- **License**: MIT

## Setup the Agent

### 1. Clone & Install Dependencies

<details>  

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-FineTuned-Agent.git

# Navigate to the project directory:
cd Coral-FineTuned-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Fine-Tune Your Model

Before using this agent, you need to create and train a fine-tuned model on your custom dataset:

<details>

**Step 1: Prepare Your Dataset**
- Collect and prepare your training data (Reddit posts, domain-specific content, etc.)
- Format your data according to the fine-tuning service requirements
- Ensure data quality and relevance to your use case

**Step 2: Fine-Tune Your Model**
- Visit [Nebius AI Studio](https://studio.nebius.com/) or your preferred fine-tuning platform
- Create an account and navigate to the fine-tuning section
- Upload your prepared dataset
- Select a base model (e.g., Llama-3.3-70B-Instruct)
- Configure training parameters and start the fine-tuning process
- Wait for training completion and note your custom model ID

**Step 3: Get API Keys**
- [Nebius AI Studio API Key](https://studio.nebius.com/api-keys)
- Your fine-tuned model ID from the training process

</details>

### 3. Configure Environment Variables

<details>

```bash
# Create .env file in project root
cp -r .env.example .env

# Add your credentials to .env file:
NEBIUS_API_KEY=your_nebius_api_key_here
FINE_TUNED_MODEL=your_custom_model_id_here
```

- Or any other fine-tuned model identifier from your chosen platform

</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seperately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  fine_tuned_agent:
    options:
      - name: "NEBIUS_API_KEY"
        type: "string"
        description: "Nebius AI Studio API key for the service"
      - name: "FINE_TUNED_MODEL"
        type: "string"
        description: "Your custom fine-tuned model ID"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "NEBIUS_API_KEY"
          from: "NEBIUS_API_KEY"
        - name: "FINE_TUNED_MODEL"
          from: "FINE_TUNED_MODEL"

```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run main.py
```

You can view the agents running in Dev Mode using the [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio) by running it separately in a new terminal.

</details>


## Example

<details>


```bash
# Input:
Interface Agent: Generate me reddit post about ai in healthcare

# Output:
It will generate 5 posts similar to the data on which it is trained.
```
</details>


## Creator Details
- **Name**: Ahsen Tahir
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)