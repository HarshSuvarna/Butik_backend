from models import (
    Users,
    Products,
    CreateStore,
    ProductVariant,
    Sizes,
    VariantSizePrice,
    Transactions,
)
from schemas import ProductBulkUpload
from datetime import datetime, timedelta
import uuid


def bulkUploadProduct(body, db, secure):
    try:
        products = body.products
        threeMonCount = 0
        sixMonCount = 0
        twelveMonCount = 0
        user = (
            db.query(
                Users.threeMonthsCredits,
                Users.sixMonthsCredits,
                Users.twelveMonthsCredits,
                Users.uid,
            )
            .filter(Users.mobile == secure[0])
            .first()
        )
        product_with_ids = []
        if len(products):
            for product in products:
                if (
                    not product["brandId"]
                    or not product["categoryId"]
                    or not product["subCategoryId"]
                    or not product["materialId"]
                    or not product["genderId"]
                    or not product["countryId"]
                ):
                    return {"status_code": 0, "message": "Operation uncessfull due to invalid inputs"}
                product["productId"] = str(uuid.uuid4())
                product["isLive"] = 0
                product["is_deleted"] = 0
                product["created_on"] = datetime.now()
                product["country_id"] = product["countryId"]
                del product["countryId"]
                if product["planName"] == "3Mon":
                    threeMonCount += 1
                    if threeMonCount > user[0]:
                        return {
                            "status_code": 0,
                            "message": "Operation unsuccessfull due to insufficient credits"
                        }
                    product["expiry"] = datetime.now().replace(
                        microsecond=0
                    ) + timedelta(days=90)
                elif product["planName"] == "6Mon":
                    if sixMonCount > user[1]:
                        return {
                            "status_code": 0,
                            "message": "Operation unsuccessfull due to insufficient credits"
                        }
                    product["expiry"] = datetime.now().replace(
                        microsecond=0
                    ) + timedelta(days=180)
                elif product["planName"] == "12Mon":
                    twelveMonCount += 1
                    if twelveMonCount > user[2]:
                        return {
                            "status_code": 0,
                            "message": "Operation unsuccessfull due to insufficient credits"
                        }
                    product["expiry"] = datetime.now().replace(
                        microsecond=0
                    ) + timedelta(days=365)
                del product["planName"]
                product_with_ids.append(Products(**product))
        db.bulk_save_objects(product_with_ids)
        db.commit()
        transaction_q = Transactions(
            transactionId=uuid.uuid4(),
            uid=user[3],
            credits_3m=threeMonCount,
            credits_6m=sixMonCount,
            credits_12m=twelveMonCount,
            totalCredits=threeMonCount + sixMonCount + twelveMonCount,
            transactionDate=datetime.now().replace(microsecond=0),
            added=0,
            description="Products Created",
        )
        db.add(transaction_q)
        db.commit()
        (
            db.query(Users)
            .filter(Users.uid == user[3])
            .update(
                {
                    Users.isSeller: 1,
                    Users.threeMonthsCredits: (int(user[0]) - threeMonCount),
                    Users.sixMonthsCredits: (int(user[1]) - sixMonCount),
                    Users.twelveMonthsCredits: (int(user[2]) - twelveMonCount),
                }
            )
        )
        db.commit()
        return {
            "status_code": 200,
            "message": "Products bulk upload successful",
            "data": products,
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status_code": 0, "message": "Operation unsuccessful", "error": str(e)}


def bulkUploadVariant(body, db):
    try:
        variants = body.variants
        spqWithIds = []
        for variant in variants:
            product_q = (
                db.query(Products)
                .filter(Products.productId == str(variant.productId))
                .first()
            )
            store_q = (
                db.query(CreateStore)
                .filter(CreateStore.storeId == str(variant.storeId))
                .first()
            )
            if product_q == None:
                return {"status_code": 0, "message": "product id not valid", "data": {}}
            elif store_q == None:
                return {"status_code": 0, "message": "store id not valid", "data": {}}
            else:
                variantId = uuid.uuid4()
                productvar_q = ProductVariant(
                    variantId=variantId,
                    productId=variant.productId,
                    colorId=variant.colorId,
                    storeId=variant.storeId,
                    is_deleted=0,
                    is_visible=1,
                    created_on=datetime.now().replace(microsecond=0),
                )
                db.add(productvar_q)
                db.commit()

                variant_q = (
                    db.query(ProductVariant.variantId)
                    .filter(ProductVariant.variantId == str(variantId))
                    .first()
                )
                for spq in variant.spqList:
                    size_q = (
                        db.query(Sizes.sizeId)
                        .filter(Sizes.sizeId == str(spq["sizeId"]))
                        .first()
                    )
                    spqWithIds.append(
                        VariantSizePrice(
                            productId=variant.productId,
                            sizeId=size_q[0],
                            storeId=variant.storeId,
                            variantId=variant_q[0],
                            price=spq["price"],
                            quantity=spq["quantity"],
                        )
                    )
                db.bulk_save_objects(spqWithIds)
                db.commit()
                spqWithIds = []
            # imgUrlL = []
            # for i in range(len(imagesUrlList)):
            #     img_url = uploadToBucket_variants(variantId, i, imagesUrlList[i])
            #     var_img_q = VariantImages(
            #         variant=variant_q,
            #         productId=productId,
            #         storeId=storeId,
            #         image_url=img_url,
            #     )
            #     db.add(var_img_q)
            #     db.commit()
            #     imgUrlL.append(img_url)
        return {
            "status_code": 200,
            "message": "variants created successfully",
            "data": variants,
        }
    except Exception as e:
        print(f"error: {str(e)}")
        return {"status_code": 0, "message": "Operation unseccessful", "error": str(e)}
