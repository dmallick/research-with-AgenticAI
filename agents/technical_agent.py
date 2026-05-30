
import json
from langchain_openai import ChatOpenAI
from state.graph_state import AgentAnalysis, GoldPredictionState
from tools.parser_utils import clean_and_parse_json  


def run_technical_agent(state: GoldPredictionState, llm: ChatOpenAI) -> dict:
    """Analyzes price charts, historic resistance levels, support levels, and technical trends."""
    context = state["scraped_content"]
    
    prompt = f"""
    You are a Quantitative Technical Commodities Trader.
    Analyze the following text for pricing trends, momentum indicators, support/resistance lines, or historic structural patterns for Gold:
    
    Source Text: {context[:4000]}
    
    Respond STRICTLY in JSON format matching this schema:
    {{
        "agent_name": "Technical Analyst Agent",
        "factors_identified": ["factor1", "factor2"],
        "sentiment": "Bullish/Bearish/Neutral",
        "impact_weight": 0.50,
        "summary": "Detailed technical support/resistance and price momentum summary."
    }}
    """
    
    response = llm.invoke(prompt)
    if not isinstance(response.content, str):
        raise TypeError(f"Expected string output from LLM, got {type(response.content)}")
        
    # Safely clean and parse the JSON string payload
    data = clean_and_parse_json(response.content)
    
    return {"sentiment_analysis": AgentAnalysis(**data)}