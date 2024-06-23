from pydantic import BaseModel, Field
from enums.enums import AudioStreamServices


class FunctionInputSong(BaseModel):
    song_name: str = Field(..., description="Name of the song you wish to play")


class FunctionInputSongOR(BaseModel):
    song_name: str = Field(..., description="Name of the song you wish to play")
    repeat_time: int = Field(
        ..., description="How many times you wanna repeat the song"
    )
