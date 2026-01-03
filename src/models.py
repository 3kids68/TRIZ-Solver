from typing import List, Optional
from pydantic import BaseModel

class EngineeringParameter(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    keywords: List[str] = []

class InventivePrinciple(BaseModel):
    id: int
    name: str
    description: str
    examples: List[str] = []

class SolutionReport(BaseModel):
    improving_parameter: EngineeringParameter
    worsening_parameter: EngineeringParameter
    suggested_principles: List[InventivePrinciple]
    strategy_note: str
    execution_log: List[str] = [] # Transparency log

class IdealityFactor(BaseModel):
    name: str
    weight: float  # 1.0 to 10.0 scale recommended
