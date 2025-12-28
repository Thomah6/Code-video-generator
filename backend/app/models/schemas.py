from pydantic import BaseModel, Field
from typing import Literal, Optional

class VideoConfig(BaseModel):
    animation_type: Literal['fractal', 'game', 'dataviz', 'art', 'simulation', 'surprise'] = 'surprise'
    duration: int = Field(default=30, ge=15, le=60)
    music_style: Literal['electro', 'lofi', 'epic', 'chill'] = 'electro'

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
    video_url: Optional[str] = None
