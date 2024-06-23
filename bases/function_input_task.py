from pydantic import BaseModel, Field
from enums.enums import TaskPriority


class FunctionInputTask(BaseModel):
    text: str = Field(..., description="Task description")
    date_time: int = Field(
        ..., description="Set date and time till the task needs to be finished"
    )
    priority: TaskPriority = Field(..., description="Priority of task")
