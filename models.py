from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class NewsAnalysis(BaseModel):
    is_closure_news: bool
    cities: list[str] = Field(default_factory=list)
    reason: Literal["air_pollution","snow","rain","war","other","unknown"] = "unknown"
    shift: Literal["morning","evening","both","unknown"] = "unknown"
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)

class FinalStatus(BaseModel):
    overall_status: Literal["closed","likely","open"]
    affected_cities: list[str]
    primary_reason: str
    reasoning: str
    last_updated: datetime