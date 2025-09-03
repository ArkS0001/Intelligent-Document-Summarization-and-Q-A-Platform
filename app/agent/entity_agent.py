from autogen import AssistantAgent
from config import LLM_CONFIG

entity_agent = AssistantAgent(
    name="EntityExtractorAgent",
    llm_config=LLM_CONFIG,
    system_message="Extract key entities (names, dates, organizations, keywords) from the document text."
)
