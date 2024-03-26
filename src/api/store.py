import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db

from src.schemas import (
    StoreCreate,
    StoreID,
    StoreU,
    StorebyCat,
    UserID,
    UserLocation,
    storebySubcat,
)
from src.services.store_method import (
    add_store,
    delete_store,
    get_store_byId,
    get_stores_by_cat,
    get_stores_by_loc,
    get_stores_by_sellerid,
    get_stores_by_subcat,
    update_store,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/get_nearest_store", tags=["Store"])
def get_stores(
    store: UserLocation,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_loc(store.latitude, store.longitude, store.max_kms, db)
    return output


@router.post("/store/get_by_sellerId", tags=["Store"])
def get_stores_by_sellerids(
    store: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_sellerid(str(store.uid), db, secure)
    return output


@router.post("/store/get_nearest_by_category", tags=["Store"])
def get_stores_by_cats(
    store: StorebyCat,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_cat(
        str(store.categoryId), store.latitude, store.longitude, store.max_kms, db
    )
    return output


@router.post("/store/get_nearest_by_subcategory", tags=["Store"])
def get_stores_by_subcats(
    store: storebySubcat,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_subcat(
        str(store.subcategoryId), store.latitude, store.longitude, store.max_kms, db
    )
    return output


@router.post("/stores/getStoreById", tags=["Store"])
def get_store_byIds(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_store_byId(str(store.storeId), db)
    return output


@router.post("/create_store", tags=["Store"])
def add_stores(
    store: StoreCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    storeId = uuid.uuid4()
    output = add_store(
        str(storeId),
        str(store.uid),
        store.storeName,
        store.wholeSellerOrRetailer,
        store.storePhone,
        store.status,
        store.storeImageURL,
        store.store_add_1,
        store.store_add_2,
        store.landmark,
        store.longitude,
        store.latitude,
        store.country,
        store.state,
        store.district,
        store.locality,
        store.subLocality,
        store.pinCode,
        store.gst,
        store.pan,
        db,
        secure,
    )
    return output


@router.put("/update_store", tags=["Store"])
def update_stores(
    storeu: StoreU,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = update_store(
        str(storeu.storeId),
        storeu.storeName,
        storeu.wholeSellerOrRetailer,
        storeu.storePhone,
        storeu.status,
        storeu.storeImageURL,
        storeu.store_add_1,
        storeu.store_add_2,
        storeu.landmark,
        storeu.longitude,
        storeu.latitude,
        storeu.country,
        storeu.state,
        storeu.district,
        storeu.locality,
        storeu.subLocality,
        storeu.pinCode,
        storeu.gst,
        storeu.pan,
        db,
        secure,
    )
    return output


@router.delete("/delete_store", tags=["Store"])
def delete_stores(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_store(str(store.storeId), db, secure)
    return output
