# Used for Pydantic/Graph state definitions
# Enforces strict data schemas for agent outputs, preventing downstream compilation errors in multi-agent handoffs.
# It uses an agent graph simulation framework compatible with modern multi-agent design patterns.


from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class AgentAnalysis(BaseModel):
    agent_name: str
    factors_identified: List[str] = Field(description="List of factors found affecting gold.")
    sentiment: str = Field(description="Bullish, Bearish, or Neutral")
    impact_weight: float = Field(description="Estimated impact weight from 0.0 to 1.0")
    summary: str

class GoldPredictionState(TypedDict):
    target_url: str
    scraped_content: str
    macro_analysis: Optional[AgentAnalysis]
    sentiment_analysis: Optional[AgentAnalysis]
    technical_analysis: Optional[AgentAnalysis]
    final_forecast: Optional[str]

