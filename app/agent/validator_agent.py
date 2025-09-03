from autogen import AssistantAgent
from config import LLM_CONFIG

validator_agent = AssistantAgent(
    name="ValidatorAgent",
    llm_config=LLM_CONFIG,
    system_message="Validate outputs from other agents. Ensure factual correctness, consistency, and clarity."
)
