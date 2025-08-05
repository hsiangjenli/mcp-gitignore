from pydantic import BaseModel, Field
from typing import List, Optional


class GitignoreGenerateRequest(BaseModel):
    templates: List[str] = Field(
        ...,
        description="List of template names to generate .gitignore for (e.g., 'python', 'node', 'visualstudiocode')",
        example=["python", "visualstudiocode", "macos"],
    )


class GitignoreGenerateResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    content: str = Field(..., description="Generated .gitignore content")


class GitignoreListResponse(BaseModel):
    templates: List[str] = Field(
        ..., description="List of available gitignore templates"
    )
