
import json
from langchain_openai import ChatOpenAI
from state.graph_state import AgentAnalysis, GoldPredictionState

def run_sentiment_agent(state: GoldPredictionState, llm: ChatOpenAI) -> dict:
    """Analyzes Geopolitical risks, market instabilities, and safe-haven demand spikes."""
    context = state["scraped_content"]
    
    prompt = f"""
    You are a Geopolitical Risk & Market Sentiment Expert.
    Analyze the following text for emotional and geopolitical triggers driving Gold as a safe-haven asset:
    - Regional conflicts or trade war signals
    - Equity market volatility or banking instabilities
    - General market fear/uncertainty metrics mentioned
    
    Source Text: {context[:4000]}
    
    Respond STRICTLY in JSON format matching this schema:
    {{
        "agent_name": "Geopolitical Sentiment Agent",
        "factors_identified": ["factor1", "factor2"],
        "sentiment": "Bullish/Bearish/Neutral",
        "impact_weight": 0.70,
        "summary": "Detailed analysis of geopolitical/sentiment trends."
    }}
    """
    
    response = llm.invoke(prompt)
    data = json.loads(str(response.content))
    return {"sentiment_analysis": AgentAnalysis(**data)}
    #data = json.loads(response.content)
    #return {"sentiment_analysis": AgentAnalysis(**data)}