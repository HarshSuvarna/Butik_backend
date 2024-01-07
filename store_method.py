import string

from models import (
    Categories,
    Countries,
    CreateStore,
    Products,
    SubCategories,
    Users,
    Brand,
    VariantSizePrice,
)
from datetime import datetime, timedelta
import asyncio
import pandas as pd
import geopy.distance
from upload_image import uploadToBucket_stores, deleteImages


def get_stores_by_loc(latitude, longitude, max_kms, db):
    store_list = pd.read_sql(
        db.query(
            Products.storeId,
            Users.name,
            CreateStore.storeName,
            CreateStore.wholeSellerOrRetailer,
            CreateStore.storePhone,
            CreateStore.store_add_1,
            CreateStore.store_add_2,
            CreateStore.landmark,
            CreateStore.latitude,
            CreateStore.longitude,
            CreateStore.country,
            CreateStore.state,
            CreateStore.district,
            CreateStore.locality,
            CreateStore.subLocality,
            CreateStore.pinCode,
            CreateStore.status,
            CreateStore.storeImageURL,
        )
        .distinct(CreateStore.storeId)
        .join(Users, Users.uid == CreateStore.uid)
        .join(Products, Products.storeId == CreateStore.storeId)
        .filter(
            CreateStore.is_deleted == 0,
            CreateStore.status != "closed",
            Products.isLive == 1,
        )
        .statement,
        db.bind,
    )
    if len(store_list) == 0:
        return {"status_code": 0, "message": "no results ss found", "data": []}
    else:
        store_list["distance"] = 0.0
        counter = 0
        user_long_lat = (latitude, longitude)
        for x in store_list["storeId"]:
            store_long_lat = (
                store_list["latitude"][counter],
                store_list["longitude"][counter],
            )
            ####print(geopy.distance.distance(store_long_lat, user_long_lat).km)
            store_list["distance"][counter] = geopy.distance.distance(
                store_long_lat, user_long_lat
            ).km
            counter += 1

        store_list = store_list[store_list["distance"] < int(max_kms)]
        store_list.sort_values(by=["distance"], ascending=True, inplace=True)

        if len(store_list) == 0:
            return {"status_code": 200, "message": "no results found", "data": []}
        else:
            store_list = store_list.to_dict(orient="records")
            return {
                "status_code": 200,
                "message": str(len(store_list)) + " results found",
                "data": store_list,
            }


def get_stores_by_cat(categoryId, latitude, longitude, max_kms, db):
    cat_q = db.query(Categories).filter(Categories.categoryId == categoryId).first()
    if cat_q == None:
        return {"status_code": 0, "message": "Category does not exist", "data": []}
    else:
        store_list = pd.read_sql(
            db.query(
                CreateStore.storeId,
                Users.name,
                CreateStore.storeName,
                CreateStore.wholeSellerOrRetailer,
                CreateStore.storePhone,
                CreateStore.store_add_1,
                CreateStore.store_add_2,
                CreateStore.landmark,
                CreateStore.latitude,
                CreateStore.longitude,
                CreateStore.country,
                CreateStore.state,
                CreateStore.district,
                CreateStore.locality,
                CreateStore.subLocality,
                CreateStore.pinCode,
                CreateStore.status,
                CreateStore.storeImageURL,
            )
            .join(Users, Users.uid == CreateStore.uid)
            .join(Products, Products.storeId == CreateStore.storeId)
            .group_by(Products.storeId)
            .filter(
                CreateStore.is_deleted == 0,
                CreateStore.status != "closed",
                Products.categoryId == categoryId,
                Products.isLive == 1,
            )
            .statement,
            db.bind,
        )
        if len(store_list) == 0:
            return {"status_code": 200, "message": "no results found", "data": []}
        else:
            store_list["distance"] = 0.0
            counter = 0
            user_long_lat = (latitude, longitude)
            for x in store_list["storeId"]:
                store_long_lat = (
                    store_list["latitude"][counter],
                    store_list["longitude"][counter],
                )
                ####print(geopy.distance.distance(store_long_lat, user_long_lat).km)
                store_list["distance"][counter] = geopy.distance.distance(
                    store_long_lat, user_long_lat
                ).km
                counter += 1

            store_list = store_list[store_list["distance"] < int(max_kms)]
            store_list.sort_values(by=["distance"], ascending=True, inplace=True)
            if len(store_list) == 0:
                return {"status_code": 200, "message": "no results found", "data": []}
            else:
                store_list = store_list.to_dict(orient="records")
                # for store in store_list:
                #     if store
                return {
                    "status_code": 200,
                    "message": str(len(store_list)) + " results found",
                    "data": store_list,
                }


def get_stores_by_subcat(subcategoryId, latitude, longitude, max_kms, db):
    cat_q = (
        db.query(SubCategories)
        .filter(SubCategories.subcategoryId == subcategoryId)
        .first()
    )
    if cat_q == None:
        return {"status_code": 0, "message": "Subcategory does not exist", "data": []}
    else:
        store_list = pd.read_sql(
            db.query(
                CreateStore.storeId,
                Users.name,
                CreateStore.storeName,
                CreateStore.wholeSellerOrRetailer,
                CreateStore.storePhone,
                CreateStore.store_add_1,
                CreateStore.store_add_2,
                CreateStore.landmark,
                CreateStore.latitude,
                CreateStore.longitude,
                CreateStore.country,
                CreateStore.state,
                CreateStore.district,
                CreateStore.locality,
                CreateStore.subLocality,
                CreateStore.pinCode,
                CreateStore.status,
                CreateStore.storeImageURL,
            )
            .join(Users, Users.uid == CreateStore.uid)
            .join(Products, Products.storeId == CreateStore.storeId)
            .group_by(Products.storeId)
            .filter(
                CreateStore.is_deleted == 0,
                CreateStore.status != "closed",
                Products.subCategoryId == subcategoryId,
                Products.isLive == 1,
            )
            .statement,
            db.bind,
        )
        if len(store_list) == 0:
            return {"status_code": 200, "message": "no results found", "data": []}
        else:
            store_list["distance"] = 0.0
            counter = 0
            user_long_lat = (latitude, longitude)
            for x in store_list["storeId"]:
                store_long_lat = (
                    store_list["latitude"][counter],
                    store_list["longitude"][counter],
                )
                ####print(geopy.distance.distance(store_long_lat, user_long_lat).km)
                store_list["distance"][counter] = geopy.distance.distance(
                    store_long_lat, user_long_lat
                ).km
                counter += 1

            store_list = store_list[store_list["distance"] < int(max_kms)]
            store_list.sort_values(by=["distance"], ascending=True, inplace=True)
            if len(store_list) == 0:
                return {"status_code": 200, "message": "no results found", "data": []}
            else:
                store_list = store_list.to_dict(orient="records")
                # for store in store_list:
                #     if store
                return {
                    "status_code": 200,
                    "message": str(len(store_list)) + " results found",
                    "data": store_list,
                }


def get_stores_by_sellerid(uid, db, secure):
    user_q = db.query(Users).filter(Users.uid == uid, Users.is_deleted == 0).first()
    if user_q != None and user_q.isSeller == True and user_q.mobile == secure[0]:
        store_q = (
            db.query(CreateStore)
            .filter(CreateStore.uid == uid, CreateStore.is_deleted == 0)
            .all()
        )
        if len(store_q) == 0:
            return {"status_code": 200, "message": "no results found", "data": []}
        else:
            store_att = [
                "storeId",
                "storeName",
                "storeImageURL",
                "district",
                "locality",
                "storePhone",
                "wholeSellerOrRetailer",
            ]
            outputList = []
            for store in store_q:
                outputList.append(store)
            return {
                "status_code": 200,
                "message": str(len(outputList)) + " results found",
                "data": outputList,
            }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": [],
        }


def get_store_byId(storeId, db):
    store_q = (
        db.query(CreateStore)
        .filter(CreateStore.storeId == storeId, CreateStore.is_deleted == 0)
        .first()
    )
    if store_q == None:
        return {"status_code": 0, "message": "Store does not exist", "data": {}}
    else:
        return {"status_code": 200, "message": "store found", "data": store_q}


def add_store(
    id,
    uid,
    storeName,
    wholeSellerOrRetailer,
    storePhone,
    status,
    storeImageURL,
    store_add_1,
    store_add_2,
    landmark,
    longitude,
    latitude,
    country,
    state,
    district,
    locality,
    subLocality,
    pinCode,
    gst,
    pan,
    db,
    secure,
):
    user_q = db.query(Users).filter(Users.uid == uid, Users.is_deleted == 0).first()
    if user_q != None and user_q.isSeller == True and user_q.mobile == secure[0]:
        imgUrl = uploadToBucket_stores(id, storeImageURL)
        new_store = CreateStore(
            storeId=id,
            status="open",
            storeName=storeName,
            storeImageURL=imgUrl,
            wholeSellerOrRetailer=wholeSellerOrRetailer,
            storePhone=storePhone,
            store_add_1=store_add_1,
            store_add_2=store_add_2,
            landmark=landmark,
            longitude=longitude,
            latitude=latitude,
            country=country,
            state=state,
            district=district,
            locality=locality,
            subLocality=subLocality,
            pinCode=pinCode,
            gst=gst,
            pan=pan,
            is_deleted=0,
            user=user_q,
            created_on=datetime.now().replace(microsecond=0),
            last_updated=None,
        )
        db.add(new_store)
        db.commit()
        db.refresh(new_store)

        store_q = (
            db.query(CreateStore.storeId).filter(CreateStore.storeId == id).first()
        )
        # print(store_q[0])
        return {
            "status_code": 200,
            "message": "store created successfully",
            "data": {
                "storeId": store_q[0],
                "uid": uid,
                "storeName": storeName,
                "wholeSellerOrRetailer": wholeSellerOrRetailer,
                "storePhone": storePhone,
                "status": "open",
                "storeImageURL": imgUrl,
                "store_add_1": store_add_1,
                "store_add_2": store_add_2,
                "landmark": landmark,
                "longitude": float(longitude),
                "latitude": float(latitude),
                "country": country,
                "state": state,
                "district": district,
                "locality": locality,
                "subLocality": subLocality,
                "pinCode": pinCode,
                "gst": gst,
                "pan": pan,
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def update_store(
    storeId,
    storeName,
    wholeSellerOrRetailer,
    storePhone,
    status,
    storeImageURL,
    store_add_1,
    store_add_2,
    landmark,
    longitude,
    latitude,
    country,
    state,
    district,
    locality,
    subLocality,
    pinCode,
    gst,
    pan,
    db,
    secure,
):
    user_q = (
        db.query(Users)
        .join(CreateStore, CreateStore.uid == Users.uid)
        .filter(
            Users.mobile == secure[0],
            Users.is_deleted == 0,
            CreateStore.storeId == storeId,
        )
        .first()
    )
    print(user_q)
    if user_q != None and user_q.isSeller == True:
        store_info = (
            db.query(CreateStore)
            .filter(CreateStore.storeId == storeId, CreateStore.is_deleted == 0)
            .first()
        )

        if store_info == None:
            return {"status_code": 0, "message": "Store does not exist", "data": {}}
        else:
            if len(storeImageURL) >= 100:
                imgUrl = uploadToBucket_stores(storeId, storeImageURL)
            else:
                imgUrl = storeImageURL
            store_info = (
                db.query(CreateStore)
                .filter(CreateStore.storeId == storeId)
                .update(
                    {
                        CreateStore.storeName: storeName,
                        CreateStore.storeImageURL: imgUrl,
                        CreateStore.wholeSellerOrRetailer: wholeSellerOrRetailer,
                        CreateStore.storePhone: storePhone,
                        CreateStore.store_add_1: store_add_1,
                        CreateStore.status: status,
                        CreateStore.store_add_2: store_add_2,
                        CreateStore.landmark: landmark,
                        CreateStore.longitude: longitude,
                        CreateStore.latitude: latitude,
                        CreateStore.country: country,
                        CreateStore.state: state,
                        CreateStore.district: district,
                        CreateStore.locality: locality,
                        CreateStore.subLocality: subLocality,
                        CreateStore.pinCode: pinCode,
                        CreateStore.gst: gst,
                        CreateStore.pan: pan,
                        CreateStore.last_updated: datetime.now().replace(microsecond=0),
                    }
                )
            )
            db.commit()

            return {
                "status_code": 200,
                "message": "store updated successfully",
                "data": {
                    "storeId": storeId,
                    "storeName": storeName,
                    "wholeSellerOrRetailer": wholeSellerOrRetailer,
                    "storePhone": storePhone,
                    "status": status,
                    "storeImageURL": imgUrl,
                    "store_add_1": store_add_1,
                    "store_add_2": store_add_2,
                    "landmark": landmark,
                    "longitude": longitude,
                    "latitude": latitude,
                    "country": country,
                    "state": state,
                    "district": district,
                    "locality": locality,
                    "subLocality": subLocality,
                    "pinCode": pinCode,
                    "gst": gst,
                    "pan": pan,
                    "status_code": 200,
                },
            }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def delete_store(storeId, db, secure):
    user_q = (
        db.query(Users)
        .join(CreateStore, CreateStore.uid == Users.uid)
        .filter(
            Users.mobile == secure[0],
            Users.is_deleted == 0,
            CreateStore.storeId == storeId,
        )
        .first()
    )

    if user_q != None and user_q.isSeller == True:
        store_q = (
            db.query(CreateStore.storeId)
            .filter(CreateStore.storeId == storeId, CreateStore.is_deleted == 0)
            .first()
        )
        if store_q == None:
            return {"status_code": 0, "message": "Store doesnt exist", "data": {}}
        else:
            store_u = (
                db.query(CreateStore)
                .filter(CreateStore.storeId == storeId)
                .update({CreateStore.is_deleted: 1})
            )
            db.commit()
            # product_d = db.query(Products).filter(Products.storeId==storeId).delete(synchronize_session=False)
            # db.commit()
            path = "storeImages/store_"
            deleteImages(storeId, path)
            return {
                "status_code": 200,
                "message": "Store deleted successfully",
                "data": {"storeId": store_q[0]},
            }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }
