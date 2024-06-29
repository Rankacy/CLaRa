from typing import List
from pydantic import BaseModel, Field
from enums.enums import Stores


class FunctionInputArray(BaseModel):
    # total_price: int = Field(...,description="Total cost of groceries")
    store: Stores = Field(..., description="Name of the store")
    item: List[str] = Field(..., description="List of grocery items")
