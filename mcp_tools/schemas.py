from pydantic import BaseModel, Field
from typing import List, Optional


class GitignoreGenerateRequest(BaseModel):
    templates: List[str] = Field(
        ...,
        description="List of template names to generate .gitignore for (e.g., 'python', 'node', 'visualstudiocode')",
        example=["python", "visualstudiocode", "macos"],
    )
    output_path: Optional[str] = Field(
        default=".gitignore",
        description="Output file path for the .gitignore file",
        example=".gitignore",
    )


class GitignoreGenerateResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    content: str = Field(..., description="Generated .gitignore content")
    file_path: str = Field(..., description="Path where the .gitignore file was saved")


class GitignoreListResponse(BaseModel):
    templates: List[str] = Field(
        ..., description="List of available gitignore templates"
    )
