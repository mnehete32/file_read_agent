from pydantic import Field, BaseModel
from langchain_core.tools import BaseTool
from typing import Type

class FileReadToolInput(BaseModel):
    file_path: str = Field(
        description="The absolute path to the file to be read."
    )

class FileReadTool(BaseTool):
    name: str = "file_read"
    description: str = "Prints a content file designated by the supplied absolute path and returns the content of the file as string."
    args_schema: Type[BaseModel] =  FileReadToolInput

    def _run(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            content = file.read()
        return content