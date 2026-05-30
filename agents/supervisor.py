
# Supervisor acts as a router or an orchestrator
# It imports the individual agents, passes the state down, and acts as the central management  --
# hub for the workflow.


import logging
from langchain_openai import ChatOpenAI
from state.graph_state import GoldPredictionState
from tools.web_scrapers import extract_url_content
from agents.macro_agent import run_macro_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.technical_agent import run_technical_agent

# Set up clean logging for orchestration visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SupervisorAgent")

def run_synthesizer(state: GoldPredictionState, llm: ChatOpenAI) -> dict:
    """
    Acts as the Chief Investment Officer node. 
    Synthesizes the parallel inputs from all expert agents.
    """
    macro = state.get("macro_analysis")
    sentiment = state.get("sentiment_analysis")
    technical = state.get("technical_analysis")
    
    #if not all([macro, sentiment, technical]):
    #    raise ValueError("Missing critical agent data required for synthesis.")

# Explicit type guard check to satisfy Pylance's type-narrowing
    if macro is None or sentiment is None or technical is None:
        raise ValueError("Missing critical agent data required for synthesis.")
    
    prompt = f"""
    You are the Chief Investment Officer. Synthesize the findings from your specialist agents to issue a final gold market prediction.
    
    
    1. Macroeconomic Evaluation:
       - Sentiment: {macro.sentiment} (Weight: {macro.impact_weight})
       - Summary: {macro.summary}
       
    2. Geopolitical & Sentiment Evaluation:
       - Sentiment: {sentiment.sentiment} (Weight: {sentiment.impact_weight})
       - Summary: {sentiment.summary}
       
    3. Technical Trend Evaluation:
       - Sentiment: {technical.sentiment} (Weight: {technical.impact_weight})
       - Summary: {technical.summary}
       
    Compile a final, professional execution report detailing the consensus vector (e.g., Strongly Bullish, Moderately Bearish), immediate trigger factors to watch, and a synthesis of the near-future gold price direction.
    """
    
    response = llm.invoke(prompt)
    return {"final_forecast": response.content}

def orchestrate_gold_prediction(url: str, llm: ChatOpenAI) -> GoldPredictionState:
    """
    The Supervisor core router loop. 
    Manages state initiation, component invocation sequencing, and error handling.
    """
    logger.info(f"Initializing prediction workflow for URL: {url}")
    
    # 1. Scraping & State initialization
    scraped_text = extract_url_content(url)
    if "Failed" in scraped_text or "Error" in scraped_text:
        logger.error(f"Data collection failed: {scraped_text}")
        raise RuntimeError(f"Workflow aborted: {scraped_text}")

    state: GoldPredictionState = {
        "target_url": url,
        "scraped_content": scraped_text,
        "macro_analysis": None,
        "sentiment_analysis": None,
        "technical_analysis": None,
        "final_forecast": None
    }
    
    # 2. Invoke Specialist Nodes (Fan-out layout)
    try:
        logger.info("Routing payload to Macroeconomic Agent...")
        state.update(run_macro_agent(state, llm))
        
        logger.info("Routing payload to Geopolitical Sentiment Agent...")
        state.update(run_sentiment_agent(state, llm))
        
        logger.info("Routing payload to Technical Analyst Agent...")
        state.update(run_technical_agent(state, llm))
        
    except Exception as e:
        logger.error(f"Error during expert agent processing phase: {str(e)}")
        raise e

    # 3. Fan-in / Synthesis Node
    logger.info("All expert states gathered. Invoking Final Synthesizer...")
    synthesis_result = run_synthesizer(state, llm)
    state.update(synthesis_result)
    
    logger.info("Workflow execution finalized successfully.")
    return state