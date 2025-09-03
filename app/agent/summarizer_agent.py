from autogen import AssistantAgent
from config import LLM_CONFIG

summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    llm_config=LLM_CONFIG,
    system_message="You are an expert at summarizing documents into structured, concise outputs."
)
