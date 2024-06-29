from pydantic import BaseModel, Field
from enums.enums import Language


class FunctionInputTranslation(BaseModel):
    text: str = Field(..., description="Text to translate")
    from_language: Language = Field(..., description="Language to translate from")
    to_language: Language = Field(..., description="Language to translate to")
