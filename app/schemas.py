from pydantic import BaseModel
from typing import List, Any


class ColumnSchema(BaseModel):
    name: str
    type: str


class UploadResponse(BaseModel):
    id: int
    name: str
    chart: str
    columns: List[ColumnSchema]


class DatasetResponse(BaseModel):
    id: int
    name: str
    chart: str
    columns: List[ColumnSchema]
    rows: List[dict[str, Any]]