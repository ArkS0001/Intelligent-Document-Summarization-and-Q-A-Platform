from autogen import AssistantAgent
from config import LLM_CONFIG

qna_agent = AssistantAgent(
    name="QnAAgent",
    llm_config=LLM_CONFIG,
    system_message="Answer questions using provided document context. Be precise and cite relevant parts."
)
