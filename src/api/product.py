import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db

from src.schemas import (
    CategoryID,
    IsLive,
    Product_id,
    ProductCreate,
    SearchProduct,
    StoreID,
)
from src.services.product_method import (
    add_product,
    delete_product,
    get_product_by_cat,
    get_product_by_id,
    get_product_by_store,
    get_product_by_store_seller,
    getSearchedProducts,
    toggleIsLive,
    update_product,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/product/get_by_store_user", tags=["Product"])
def get_products_by_stores(
    product: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_store(str(product.storeId), db)
    return output


@router.post("/product/get_by_store_seller", tags=["Product"])
def get_products_by_store_sellers(
    product: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_store_seller(str(product.storeId), db, secure)
    return output


@router.post("/product/get_by_productId", tags=["Product"])
def get_products_by_id(
    product: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_id(str(product.productId), db)
    return output


@router.post("/product/get_by_categoryId", tags=["Product"])
def get_products_by_cats(
    product: CategoryID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_cat(
        str(product.categoryId),
        product.latitude,
        product.longitude,
        product.max_kms,
        db,
    )
    return output


@router.post("/product/toggleProductLiveStatus", tags=["Product"])
def toggleIsLives(
    product: IsLive,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = toggleIsLive(str(product.productId), product.isLive, db, secure)
    return output


@router.post("/create_product", tags=["Product"])
def add_products(
    product: ProductCreate, db: Session = Depends(get_db)
):  # , secure=Depends(auth_handler.auth_wrapper)):
    productId = uuid.uuid4()
    output = add_product(
        str(productId),
        str(product.brandId),
        str(product.categoryId),
        product.productName,
        product.productDescription,
        str(product.materialId),
        str(product.storeId),
        str(product.subCategoryId),
        str(product.countryId),
        str(product.genderId),
        product.productImageUrl,
        str(product.uid),
        product.planName,
        db,
    )
    return output


@router.put("/update_product", tags=["Product"])
def update_products(
    product: SearchProduct,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = update_product(
        str(product.productId),
        str(product.brandId),
        str(product.categoryId),
        product.productName,
        product.productDescription,
        str(product.materialId),
        str(product.storeId),
        str(product.subCategoryId),
        str(product.countryId),
        str(product.genderId),
        product.productImageUrl,
        product.isLive,
        db,
        secure,
    )
    return output


@router.delete("/delete_product", tags=["Product"])
def delete_products(
    product: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_product(str(product.productId), db, secure)
    return output


@router.post("/get-searched-products", tags=["Product"])
def searchedProducts(
    body: SearchProduct,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getSearchedProducts(body, db, secure)
    print("output", output)
    return output
