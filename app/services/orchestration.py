from app.agents.summarizer_agent import summarizer_agent
from app.agents.entity_agent import entity_agent
from app.agents.qna_agent import qna_agent
from app.agents.validator_agent import validator_agent

def run_summarization(text: str) -> str:
    result = summarizer_agent.run(text)
    validated = validator_agent.run(f"Validate this summary:\n{result}")
    return validated

def run_entity_extraction(text: str) -> str:
    result = entity_agent.run(text)
    validated = validator_agent.run(f"Validate these entities:\n{result}")
    return validated

def run_qna(query: str, context: str) -> str:
    result = qna_agent.run(f"Context:\n{context}\n\nQuestion: {query}")
    validated = validator_agent.run(f"Validate this answer:\n{result}")
    return validated
