
# Handles Macroeconomic factors that impacts the Gold Prices

import json
from langchain_openai import ChatOpenAI
from state.graph_state import AgentAnalysis, GoldPredictionState

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
    data = json.loads(str(response.content))
    #data = json.loads(response.content)
    return {"macro_analysis": AgentAnalysis(**data)}