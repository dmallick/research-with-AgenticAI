
# Handles Macroeconomic factors that impacts the Gold Prices

import json
from langchain_openai import ChatOpenAI
from state.graph_state import AgentAnalysis, GoldPredictionState
from tools.parser_utils import clean_and_parse_json

def run_macro_agent(state: GoldPredictionState, llm: ChatOpenAI) -> dict:
    """Analyzes Inflation, Interest Rates, Dollar Index (DXY), and Central Bank behaviors."""
    context = state["scraped_content"]
    
    prompt = f"""
    You are an expert Macroeconomic Analyst specializing in global precious metals.
    Analyze the following text specifically for macroeconomic drivers affecting Gold prices:
    - Interest rate cycles (Fed policies)
    - Currency performance (specifically US Dollar strength/weakness)
    - Inflation or deflation signals
    
    Source Text: {context[:4000]}
    
    Respond STRICTLY in JSON format matching this schema:
    {{
        "agent_name": "Macroeconomic Agent",
        "factors_identified": ["factor1", "factor2"],
        "sentiment": "Bullish/Bearish/Neutral",
        "impact_weight": 0.85,
        "summary": "Detailed macroeconomic insight here."
    }}
    """
    
    response = llm.invoke(prompt)
    if not isinstance(response.content, str):
        raise TypeError(f"Expected string output from LLM, got {type(response.content)}")
        
    # Safely clean and parse the JSON string payload
    data = clean_and_parse_json(response.content)
    
    return {"sentiment_analysis": AgentAnalysis(**data)}