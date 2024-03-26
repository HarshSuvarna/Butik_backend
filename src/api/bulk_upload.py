import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db

from src.schemas import BulkUploadProductCreate, BulkUploadVariantCreate
from src.services.bulk_upload_method import bulkUploadProduct, bulkUploadVariant

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/bulk-upload/products", tags=["Bulk Uploads"])
def bulkUploadProducts(
    body: BulkUploadProductCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return bulkUploadProduct(body, db, secure)


@router.post("/bulk-upload/variants", tags=["Bulk Uploads"])
def bulkUploadVariants(
    body: BulkUploadVariantCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return bulkUploadVariant(body, db)
