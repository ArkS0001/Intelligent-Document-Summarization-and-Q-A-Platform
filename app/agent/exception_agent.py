from autogen import AssistantAgent
from config import LLM_CONFIG

exception_agent = AssistantAgent(
    name="ExceptionAgent",
    llm_config=LLM_CONFIG,
    system_message="Handle errors gracefully and suggest fixes for failed agent tasks."
)
