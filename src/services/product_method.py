from src.db.models import (
    Brand,
    Categories,
    Countries,
    CreateStore,
    Genders,
    Materials,
    ProductVariant,
    Products,
    SubCategories,
    VariantSizePrice,
    Users,
)
import geopy.distance
from datetime import datetime, timedelta
from sqlalchemy import func, true
import pandas as pd
import geopy.distance
import uuid
from src.db.models import Transactions
from src.helper.upload_image import uploadToBucket_products, deleteImages


def get_product_by_store(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId == storeId).first()
    if store_q == None:
        return {"status_code": 200, "message": "No result found", "data": []}
    else:
        product_q = (
            db.query(
                Products.productId,
                Products.productName,
                Products.imagesUrl,
                Brand.brandName,
                Products.productDescription,
                Products.isLive,
                Products.storeId,
                CreateStore.storeName,
            )
            .join(Brand, Brand.brandId == Products.brandId)
            .join(CreateStore, CreateStore.storeId == Products.storeId)
            .filter(
                Products.storeId == storeId,
                Products.is_deleted == 0,
                Products.isLive == 1,
            )
            .order_by(Products.productId)
            .all()
        )
        variant_q = (
            db.query(VariantSizePrice.productId, func.min(VariantSizePrice.price))
            .group_by(VariantSizePrice.productId)
            .order_by(VariantSizePrice.productId)
            .filter(VariantSizePrice.storeId == storeId)
            .all()
        )

        if len(product_q) == 0 or len(variant_q) == 0:
            return {"status_code": 200, "message": "No result found", "data": []}
        else:
            outputList = []

            for (
                product
            ) in product_q:  # does not return those products whos variant are not made
                for i in range(len(variant_q)):
                    if product[0] != variant_q[i][0]:
                        pass
                    else:
                        if product[5] == 0:
                            is_live = False
                        else:
                            is_live = True
                        products = {
                            "productId": product[0],
                            "storeId": product[6],
                            "storeName": product[7],
                            "productName": product[1],
                            "productDescription": product[4],
                            "productImageUrl": product[2],
                            "brandName": product[3],
                            "priceMin": variant_q[i][1],
                            "isLive": is_live,
                        }
                        outputList.append(products)
                        break

            return {
                "status_code": 200,
                "message": str(len(outputList)) + " results found",
                "data": outputList,
            }


def get_product_by_store_seller(storeId, db, secure):
    store_q = (
        db.query(CreateStore.country, Users.mobile)
        .join(Users, Users.uid == CreateStore.uid)
        .filter(CreateStore.storeId == storeId, Users.mobile == secure[0])
        .distinct(CreateStore.storeId)
        .all()
    )
    if len(store_q) > 0:
        product_q = (
            db.query(
                Products.productId,
                Products.productName,
                Products.imagesUrl,
                Brand.brandName,
                Products.productDescription,
                Products.isLive,
                Products.storeId,
                CreateStore.storeName,
            )
            .join(Brand, Brand.brandId == Products.brandId)
            .join(CreateStore, CreateStore.storeId == Products.storeId)
            .filter(Products.storeId == storeId, Products.is_deleted == 0)
            .order_by(Products.productId)
            .all()
        )
        if len(product_q) == 0:
            return {"status_code": 200, "message": "No results found", "data": []}
        else:
            outputList = []

            for product in product_q:
                variant_q = (
                    db.query(
                        VariantSizePrice.productId, func.min(VariantSizePrice.price)
                    )
                    .group_by(VariantSizePrice.productId)
                    .filter(VariantSizePrice.productId == product[0])
                    .first()
                )
                # does not return those products whos variant are not made
                if product[5] == 0:
                    is_live = False
                else:
                    is_live = True
                if variant_q == None:
                    products = {
                        "productId": product[0],
                        "storeId": product[6],
                        "storeName": product[7],
                        "productName": product[1],
                        "productDescription": product[4],
                        "productImageUrl": product[2],
                        "brandName": product[3],
                        "priceMin": 0,
                        "isLive": is_live,
                    }
                    outputList.append(products)
                else:
                    products = {
                        "productId": product[0],
                        "storeId": product[6],
                        "storeName": product[7],
                        "productName": product[1],
                        "productDescription": product[4],
                        "productImageUrl": product[2],
                        "brandName": product[3],
                        "priceMin": variant_q[1],
                        "isLive": is_live,
                    }
                    outputList.append(products)

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


def get_product_by_id(productId, db):
    product_q = (
        db.query(Products)
        .filter(Products.productId == productId, Products.is_deleted == 0)
        .first()
    )
    if product_q == None:
        return {"status_code": 0, "message": "Product doesnt exist", "data": {}}
    else:
        product_q = (
            db.query(
                Products.productId,
                Products.productName,
                Products.imagesUrl,
                Brand.brandName,
                Products.productDescription,
                Products.isLive,
                Products.storeId,
                Products.brandId,
                Categories.categoryName,
                Categories.categoryId,
                Materials.material,
                Products.materialId,
                SubCategories.subcategoryName,
                Products.subCategoryId,
                Genders.gender,
                Products.genderId,
                Countries.country,
                Products.country_id,
                Products.uid,
                Products.productDescription,
                CreateStore.storeName,
            )
            .join(Brand, Brand.brandId == Products.brandId)
            .join(Categories, Categories.categoryId == Products.categoryId)
            .join(Materials, Materials.materialId == Products.materialId)
            .join(SubCategories, SubCategories.subcategoryId == Products.subCategoryId)
            .join(Genders, Genders.genderId == Products.genderId)
            .join(Countries, Countries.countryId == Products.country_id)
            .join(CreateStore, CreateStore.storeId == Products.storeId)
            .filter(Products.productId == productId, Products.is_deleted == 0)
            .order_by(Products.productId)
            .first()
        )
        variant_q = (
            db.query(VariantSizePrice.productId, func.min(VariantSizePrice.price))
            .group_by(VariantSizePrice.productId)
            .order_by(VariantSizePrice.productId)
            .filter(VariantSizePrice.productId == productId)
            .all()
        )
        if product_q[5] == 0:
            is_live = False
        else:
            is_live = True
        if len(variant_q) == 0:
            return {
                "status_code": 200,
                "message": "product found",
                "data": {
                    "productId": product_q[0],
                    "storeId": product_q[6],
                    "productName": product_q[1],
                    "productDescription": product_q[19],
                    "productImageUrl": product_q[2],
                    "storeName": product_q[20],
                    "brandId": product_q[7],
                    "brandName": product_q[3],
                    "categoryId": product_q[9],
                    "categoryName": product_q[8],
                    "materialId": product_q[11],
                    "material": product_q[10],
                    "subCategoryId": product_q[13],
                    "subCategoryName": product_q[12],
                    "genderId": product_q[15],
                    "gender": product_q[14],
                    "countryId": product_q[17],
                    "country": product_q[16],
                    "uid": product_q[18],
                    "priceMin": 0,
                    "isLive": is_live,
                },
            }
        else:
            return {
                "status_code": 200,
                "message": "product found",
                "data": {
                    "productId": product_q[0],
                    "storeId": product_q[6],
                    "productName": product_q[1],
                    "productDescription": product_q[19],
                    "productImageUrl": product_q[2],
                    "storeName": product_q[20],
                    "brandId": product_q[7],
                    "brandName": product_q[3],
                    "categoryId": product_q[9],
                    "categoryName": product_q[8],
                    "materialId": product_q[11],
                    "material": product_q[10],
                    "subCategoryId": product_q[13],
                    "subCategoryName": product_q[12],
                    "genderId": product_q[15],
                    "gender": product_q[14],
                    "countryId": product_q[17],
                    "country": product_q[16],
                    "uid": product_q[18],
                    "priceMin": variant_q[0][1],
                    "isLive": is_live,
                },
            }


def get_product_by_cat(categoryId, latitude, longitude, max_kms, db):
    cat_q = db.query(Categories).filter(Categories.categoryId == categoryId).first()
    if cat_q == None:
        return {"status_code": 0, "message": "Category does not exist", "data": []}
    else:
        store_list = pd.read_sql(
            db.query(CreateStore.storeId, CreateStore.latitude, CreateStore.longitude)
            .filter(CreateStore.is_deleted == 0, CreateStore.status == "open")
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
                store_list["distance"][counter] = geopy.distance.distance(
                    store_long_lat, user_long_lat
                ).km
                counter += 1
            storeIdList = store_list[store_list["distance"] < int(max_kms)][
                "storeId"
            ].to_list()

        product_q = (
            db.query(
                Products.productId,
                Products.productName,
                Products.imagesUrl,
                Brand.brandName,
                Products.productDescription,
                Products.storeId,
            )
            .join(Brand, Brand.brandId == Products.brandId)
            .filter(
                Products.categoryId == categoryId,
                Products.is_deleted == 0,
                Products.isLive == 1,
                Products.storeId.in_(storeIdList),
            )
            .order_by(Products.productId)
            .all()
        )

        if len(product_q) == 0:
            return {"status_code": 200, "message": "no results found", "data": []}
        else:
            count = 0
            outputList = (
                []
            )  # The proudct will be displayed only if the variant and SQP is available
            for product in product_q:
                variant_q = (
                    db.query(
                        VariantSizePrice.productId, func.min(VariantSizePrice.price)
                    )
                    .group_by(VariantSizePrice.productId)
                    .filter(VariantSizePrice.productId == product[0])
                    .all()
                )
                if len(variant_q) != 0:
                    products = {
                        "id": product[0],
                        "ProductName": product[1],
                        "storeId": product[5],
                        "productImageUrl": product[2],
                        "brandName": product[3],
                        "productDescription": product[4],
                        "priceMin": variant_q[0][1],
                    }
                    outputList.append(products)
                count += 1
            return {
                "status_code": 200,
                "message": str(len(outputList)) + " results found",
                "data": outputList,
            }


def add_product(
    productId,
    brandId,
    categoryId,
    productName,
    productDescription,
    materialId,
    storeId,
    subCategoryId,
    country_id,
    genderId,
    imagesUrl,
    uid,
    planName,
    db,
):
    store_q = db.query(CreateStore).filter(CreateStore.storeId == storeId).first()
    user_q = (
        db.query(
            Users.threeMonthsCredits, Users.sixMonthsCredits, Users.twelveMonthsCredits
        )
        .filter(Users.uid == uid)
        .first()
    )
    threeMonCredit = 0
    sixMonCredit = 0
    twelveMonCredit = 0
    if store_q == None:
        return {"status_code": 0, "message": "Store ID not valid", "data": {}}
    elif user_q == None:
        return {"status_code": 0, "message": "User ID not valid", "data": {}}
    else:
        if planName == "3Mon" and (user_q[0] != 0):
            threeMonCredit = 1
            trans = (
                db.query(Users)
                .filter(Users.uid == uid)
                .update(
                    {Users.isSeller: 1, Users.threeMonthsCredits: (int(user_q[0]) - 1)}
                )
            )
            db.commit()
            expiry = datetime.now().replace(microsecond=0) + timedelta(days=90)
        elif planName == "6Mon" and (user_q[1] != 0):
            sixMonCredit = 1
            trans = (
                db.query(Users)
                .filter(Users.uid == uid)
                .update(
                    {Users.isSeller: 1, Users.sixMonthsCredits: (int(user_q[1]) - 1)}
                )
            )
            db.commit()
            expiry = datetime.now().replace(microsecond=0) + timedelta(days=180)
        elif planName == "12Mon" and (user_q[2] != 0):
            twelveMonCredit = 1
            trans = (
                db.query(Users)
                .filter(Users.uid == uid)
                .update(
                    {Users.isSeller: 1, Users.twelveMonthsCredits: (int(user_q[2]) - 1)}
                )
            )
            db.commit()
            expiry = datetime.now().replace(microsecond=0) + timedelta(days=365)
        else:
            return {
                "status_code": 0,
                "message": "Product cannot be created due to insufficient Credit balance",
                "data": {},
            }

        imgUrl = uploadToBucket_products(productId, imagesUrl)
        product_q = Products(
            productId=productId,
            brandId=brandId,
            categoryId=categoryId,
            productName=productName,
            productDescription=productDescription,
            materialId=materialId,
            storeId=storeId,
            subCategoryId=subCategoryId,
            country_id=country_id,
            genderId=genderId,
            imagesUrl=imgUrl,
            isLive=0,
            is_deleted=0,
            uid=uid,
            created_on=datetime.now(),
            expiry=expiry,
        )
        db.add(product_q)
        db.commit()

        transactionId = uuid.uuid4()
        transaction_q = Transactions(
            transactionId=transactionId,
            uid=uid,
            credits_3m=threeMonCredit,
            credits_6m=sixMonCredit,
            credits_12m=twelveMonCredit,
            totalCredits=1,
            transactionDate=datetime.now().replace(microsecond=0),
            added=0,
            description="Product Created",
            productId=productId,
        )
        db.add(transaction_q)
        db.commit()

        return {
            "status_code": 200,
            "message": "Product Created Successfully",
            "data": {
                "productId": productId,
                "brandId": brandId,
                "categoryId": categoryId,
                "productName": productName,
                "productDescription": productDescription,
                "materialId": materialId,
                "storeId": storeId,
                "uid": uid,
                "subCategoryId": subCategoryId,
                "countryId": country_id,
                "genderId": genderId,
                "productImageUrl": imgUrl,
                "isLive": False,
            },
        }


def update_product(
    productId,
    brandId,
    categoryId,
    productName,
    productDescription,
    materialId,
    storeId,
    subCategoryId,
    country_id,
    genderId,
    imagesUrl,
    isLive,
    db,
    secure,
):
    product_q = (
        db.query(Products.productId, Users.mobile)
        .join(Users, Users.uid == Products.uid)
        .filter(Products.productId == productId, Users.mobile == secure[0])
        .first()
    )
    if len(product_q) > 0:
        if imagesUrl and len(imagesUrl) >= 100:
            imgUrl = uploadToBucket_products(storeId, imagesUrl)
        else:
            imgUrl = imagesUrl
        if isLive == False:
            is_live = 0
        else:
            is_live = 1
        product_q = (
            db.query(Products)
            .filter(Products.productId == productId)
            .update(
                {
                    Products.productName: productName,
                    Products.isLive: is_live,
                    Products.imagesUrl: imgUrl,
                    Products.materialId: materialId,
                    Products.productDescription: productDescription,
                    Products.categoryId: categoryId,
                    Products.subCategoryId: subCategoryId,
                    Products.brandId: brandId,
                    Products.storeId: storeId,
                    Products.genderId: genderId,
                    Products.country_id: country_id,
                    Products.updated_on: datetime.now().replace(microsecond=0),
                }
            )
        )
        db.commit()
        return {
            "status_code": 200,
            "message": "Product updated Successfully",
            "data": {
                "productId": productId,
                "brandId": brandId,
                "categoryId": categoryId,
                "productName": productName,
                "productDescription": productDescription,
                "materialId": materialId,
                "storeId": storeId,
                "subCategoryId": subCategoryId,
                "countryId": country_id,
                "genderId": genderId,
                "productImageUrl": imgUrl,
                "isLive": isLive,
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def getSearchedProducts(body, db, secure):
    userPosition = (body.latitude, body.longitude)
    product_q = (
        db.query(
            Products.productId,
            Products.productName,
            CreateStore.latitude,
            CreateStore.longitude,
            Products.imagesUrl,
        )
        .join(CreateStore, CreateStore.storeId == Products.storeId)
        .filter(Products.productName.like("%{}%".format(body.searchedProduct)))
        .all()
    )
    result = []
    for product in product_q:
        storePostion = (product[2], product[3])
        distance = geopy.distance.distance(userPosition, storePostion).km
        store_dict = {
            "productId": product[0],
            "productName": product[1],
            "distance": distance,
            "imageUrl": product[4],
        }
        result.append(store_dict)
    return result


def delete_product(productId, db, secure):
    product_q = (
        db.query(Products.productId, Users.mobile, Products.imagesUrl)
        .join(Users, Users.uid == Products.uid)
        .filter(Products.productId == productId)
        .first()
    )
    if product_q:
        product_u = (
            db.query(Products)
            .filter(Products.productId == productId)
            .update({Products.is_deleted: 1})
        )
        db.commit()
        # variant_d = db.query(ProductVariant).filter(ProductVariant.productId==productId).delete(synchronize_session=False)
        # db.commit()
        if product_q[2]:
            path = "productImages/product_"
            deleteImages(productId, path)
        return {
            "status_code": 200,
            "Message": "Product deleted successfully",
            "data": {"productId": product_q[0]},
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def toggleIsLive(productId, isLive, db, secure):
    product_q = (
        db.query(Products.uid, Users.mobile)
        .join(Users, Users.uid == Products.uid)
        .filter(
            Products.productId == productId,
            Products.is_deleted == 0,
            Users.mobile == secure[0],
        )
        .all()
    )
    if len(product_q) > 0:
        if isLive == False:
            is_live = 0
        else:
            is_live = 1
        product_q = (
            db.query(Products)
            .filter(Products.productId == productId)
            .update({Products.isLive: is_live})
        )
        db.commit()
        return {
            "status_code": 200,
            "Message": "isLive status updated successfully",
            "data": {},
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }
