from pydantic import BaseModel, Field

class StoryScore(BaseModel):
    industry_impact: float = Field(..., ge=0, le=10, description="Impact on the AI industry")
    technical_significance: float = Field(..., ge=0, le=10, description="Technical breakthrough or advancement")
    audience_interest: float = Field(..., ge=0, le=10, description="Interest to the AI community")
    novelty: float = Field(..., ge=0, le=10, description="New information or old news")
    overall_importance: float = Field(..., ge=0, le=10, description="Combined importance")
    reason: str = Field(..., description="Brief justification for the score")