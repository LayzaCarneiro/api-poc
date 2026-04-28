from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd

from .database import SessionLocal
from .models import Dataset
from .services import detect_schema, build_cube
from .schemas import UploadResponse, DatasetResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    df = pd.read_csv(file.file, sep=",")
    schema, chart = detect_schema(df)

    dataset = Dataset(
        name=file.filename,
        schema_json=schema,
        rows_json = (
            df.astype(object)
            .where(pd.notnull(df), None)
            .to_dict(orient="records")
        ),
        chart_type=chart
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {
        "id": dataset.id,
        "name": dataset.name,
        "chart": chart,
        "columns": schema
    }


@router.get("/datasets/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    return {
        "id": dataset.id,
        "name": dataset.name,
        "chart": dataset.chart_type,
        "columns": dataset.schema_json,
        "rows": dataset.rows_json
    }


@router.get("/datasets/{dataset_id}/cube")
def get_cube(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    return build_cube(
        dataset.rows_json,
        dataset.schema_json
    )