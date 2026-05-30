
import json
from langchain_openai import ChatOpenAI
from state.graph_state import AgentAnalysis, GoldPredictionState

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
    #data = json.loads(response.content)
    data = json.loads(str(response.content))
    return {"technical_analysis": AgentAnalysis(**data)}