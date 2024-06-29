from typing import Optional
from pydantic import BaseModel, Field
from enums.enums import UnitTypes


class FunctionInput(BaseModel):
    city: str = Field(..., description="City for whom you wanna know the weather")
    unit: Optional[UnitTypes] = Field(UnitTypes.CELSIUS, description="Temperature unit")


class FunctionInputNumber(BaseModel):
    number: int = Field(..., description="Number you wanna call")
