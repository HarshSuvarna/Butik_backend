import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db
from src.services.filter_att_method import (
    get_brand,
    get_category,
    get_color,
    get_country,
    get_gender,
    get_material,
    get_maxprice,
    get_size,
    get_sub_category,
    scope_store,
    scope_store_modified,
)
from src.services.filter_method import product_filter
from src.schemas import ProductFilter, StoreCatId, StoreID

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/filter_variants", tags=["Filters"])
def product_filters(
    filter: ProductFilter,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = product_filter(
        str(filter.storeId),
        str(filter.brandId),
        str(filter.colorId),
        str(filter.sizeId),
        str(filter.materialId),
        str(filter.categoryId),
        str(filter.subcategoryId),
        str(filter.genderId),
        filter.maxPrice,
        db,
    )
    return output


@router.post("/scope_of_store_filters", tags=["Filters"])
def scope_stores(
    storeCat: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = scope_store(str(storeCat.storeId), str(storeCat.categoryId), db)
    return output


@router.post("/scope_of_store_filters_modified", tags=["Filters"])
def scope_stores_modifieds(
    storeCat: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = scope_store_modified(str(storeCat.storeId), str(storeCat.categoryId), db)
    return output


@router.post("/brand_in_store", tags=["Filters"])
def get_brands(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_brand(str(store.storeId), db)
    return output


@router.post("/category_in_store", tags=["Filters"])
def get_categories(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_category(str(store.storeId), db)
    return output


@router.post("/subcategory_in_store", tags=["Filters"])
def get_categories(
    store: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_sub_category(str(store.storeId), str(store.categoryId), db)
    return output


@router.post("/size_in_store", tags=["Filters"])
def get_sizes(
    store: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_size(str(store.storeId), str(store.categoryId), db)
    return output


@router.post("/material_in_store", tags=["Filters"])
def get_materials(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_material(str(store.storeId), db)
    return output


@router.post("/color_in_store", tags=["Filters"])
def get_colors(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_color(str(store.storeId), db)
    return output


@router.post("/price_in_store", tags=["Filters"])
def get_prices(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_maxprice(str(store.storeId), db)
    return output


@router.post("/gender_in_store", tags=["Filters"])
def get_genders(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_gender(str(store.storeId), db)
    return output


@router.post("/country_in_store", tags=["Filters"])
def get_countries(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_country(str(store.storeId), db)
    return output


# @router.get('/get_cgender', tags=['testtt'])
# def get_couponCodes(db:Session=Depends(get_db)):#, secure=Depends(auth_handler.auth_wrapper)):
#     output = db.query(models.Brand).filter(models.Brand.is_custom).all()
#     return output

# @router.get('/put_gendef', tags=['testtt'])
# def get_couponCodes(something, is_custom ,db:Session=Depends(get_db)):#, secure=Depends(auth_handler.auth_wrapper)):
#     output = models.TEst(something=something, is_custom=is_custom)
#     db.add(output)
#     db.commit()
#     return output
