import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db

from src.schemas import (
    Product_id,
    SqpD,
    VariantCreate,
    VariantID,
    VariantImageD,
    VariantUpdate,
)
from src.services.variant_method import (
    add_variant,
    delete_variant,
    delete_variant_image,
    delete_variant_size,
    get_variant_by_id,
    get_variant_image,
    get_variantList_by_id,
    update_variant,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/getDetailedProductForUser", tags=["Product Variants"])
def get_variant_by_ids(
    variant: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_variant_by_id(str(variant.productId), db)
    return output


@router.post("/getVariantListByProductId", tags=["Product Variants"])
def get_variantList_by_ids(
    variant: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_variantList_by_id(str(variant.productId), db)
    return output


"""
@user.post('/variant/get_by_variant', tags=['Product Variants'])
def get_variants(variant:VariantID, db:Session=Depends(get_db)):#, secure=Depends(auth_handler.auth_wrapper)):
    output = get_variant(variant.variantId, db)
    return output
"""


@router.post("/create_variant", tags=["Product Variants"])
def add_variants(
    variant: VariantCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    variantId = uuid.uuid4()
    output = add_variant(
        str(variantId),
        str(variant.productId),
        str(variant.storeId),
        str(variant.colorId),
        variant.spqList,
        variant.imagesUrlList,
        db,
    )
    return output


@router.put("/update_variant", tags=["Product Variants"])
def update_variants(
    variant: VariantUpdate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = update_variant(
        str(variant.variantId),
        str(variant.productId),
        str(variant.storeId),
        str(variant.colorId),
        variant.spqList,
        variant.imagesUrlList,
        db,
    )
    return output


@router.post("/get_varinat_images", tags=["Product Variants"])
def get_variant_images(
    variant: VariantImageD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_variant_image(variant.imageUrl, db)
    return output


@router.delete("/delete_variant", tags=["Product Variants"])
def delete_variants(
    variant: VariantID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_variant(str(variant.variantId), db)
    return output


@router.delete("/delete_variant_images", tags=["Product Variants"])
def delete_variant_images(
    variant: VariantImageD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_variant_image(variant.imageUrl, db)
    return output


@router.delete("/delete_variant_size", tags=["Product Variants"])
def delete_variant_sizes(
    size: SqpD, db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = delete_variant_size(str(size.sqpId), db)
    return output
