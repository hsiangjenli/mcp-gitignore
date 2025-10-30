from pydantic import BaseModel, Field
from typing import List, Optional


class GitignoreGenerateRequest(BaseModel):
    templates: List[str] = Field(
        ...,
        description="List of template names to generate .gitignore for (e.g., 'python', 'node', 'visualstudiocode')",
        json_schema_extra={"example": ["python", "visualstudiocode", "macos"]},
    )
    existing_content: Optional[str] = Field(
        None,
        description="Existing .gitignore content to merge with. If provided, only new patterns will be added.",
    )


class GitignoreGenerateResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    content: str = Field(..., description="Generated .gitignore content")
    patterns_added: Optional[int] = Field(
        None,
        description="Number of new patterns added (when merging with existing content)",
    )


class GitignoreListResponse(BaseModel):
    templates: List[str] = Field(
        ..., description="List of available gitignore templates"
    )
