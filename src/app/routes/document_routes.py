from typing import List, Optional

from fastapi import APIRouter

from app.models.document_model import Document
from app.repositories.document_repository import DocumentRepository

document_router = APIRouter()


@document_router.get("/", response_model=List[Document], tags=["Document"])
async def get_list() -> List[Document]:
    documents = await DocumentRepository.get_list()
    return documents


@document_router.get("/{document_id}", response_model=Document, tags=["Document"])
async def get_document(document_id: int) -> Optional[Document]:
    document = await DocumentRepository.get_by_id(document_id)
    return document


@document_router.put("/create", response_model=Document, tags=["Document"])
async def create_document(document: Document):
    document = await DocumentRepository.upsert(document)
    return document


@document_router.delete("/delete/{document_id}", tags=["Document"])
async def delete_document(document_id: int) -> bool:
    response = await DocumentRepository.delete(document_id)
    return response
