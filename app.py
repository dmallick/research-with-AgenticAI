
# Entry Point

import os
from langchain_openai import ChatOpenAI
from agents.supervisor import orchestrate_gold_prediction

def main():
    # Enforce API key verification
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    
    # Target context URL
    target_market_url = "https://www.reuters.com/markets/commodities/"
    
    try:
        # Hand off complete execution block to the supervisor
        final_state = orchestrate_gold_prediction(target_market_url, llm)
        
        print("\n================== FINAL GOLD MARKET FORECAST REPORT ==================\n")
        print(final_state["final_forecast"])
        print("\n=======================================================================\n")
        
    except Exception as e:
        print(f"Pipeline Execution Failed: {str(e)}")

if __name__ == "__main__":
    main()