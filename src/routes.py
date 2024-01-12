from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from sqlalchemy import true
import models
from database import engine, SessionLocal
import uuid
from authenticate import AuthHandler
from schemas import (
    CategoryID,
    CategoryIDD,
    CategoryNames,
    BrandNames,
    GetSizes,
    CountryNames,
    GenderNames,
    ColorNames,
    MaterialNames,
    IsLive,
    Product_id,
    ProductCreate,
    ProductFilter,
    ProductU,
    SqpD,
    StoreCreate,
    StoreID,
    StoreU,
    StorebyCat,
    TransactionC,
    TransactionID,
    User_basic,
    UserID,
    UserLocation,
    VariantCreate,
    VariantID,
    VariantImageD,
    VariantUpdate,
    VerifyOtp,
    UpdateUser,
    UserCreate,
    StoreCatId,
    storebySubcat,
    BulkUploadProductCreate,
    BulkUploadVariantCreate,
    SearchProduct,
)
from OTP_verification import send_otp, verify_otp
from user_method import (
    add_user,
    update_user,
    delete_user,
    get_user,
    get_user_bytoken,
    user_to_seller,
)
from store_method import (
    add_store,
    delete_store,
    get_stores_by_subcat,
    update_store,
    get_stores_by_loc,
    get_stores_by_cat,
    get_stores_by_sellerid,
    get_store_byId,
)
from product_method import (
    add_product,
    get_product_by_cat,
    update_product,
    delete_product,
    get_product_by_store,
    get_product_by_id,
    get_product_by_store_seller,
    toggleIsLive,
    getSearchedProducts,
)
from variant_method import (
    add_variant,
    update_variant,
    delete_variant_image,
    delete_variant,
    delete_variant_size,
    get_variant_image,
    get_variant_by_id,
    get_variantList_by_id,
)
from filter_att_method import (
    get_brand,
    get_category,
    get_sub_category,
    get_size,
    get_color,
    get_material,
    get_maxprice,
    get_country,
    get_gender,
    scope_store,
    scope_store_modified,
)
from filter_method import product_filter
from transaction_method import (
    post_transaction,
    get_transaction,
    get_couponCode,
    getCreditBalance,
)
from attribute_method import (
    get_all_brands,
    get_subcat_by_cat,
    getAllcategory,
    getAllSize,
    getAllMaterial,
    getAllColor,
    getAllCountry,
    getAllgender,
)
from bulk_upload import bulkUploadProduct, bulkUploadVariant

user = APIRouter()
models.Base.metadata.create_all(engine)
auth_handler = AuthHandler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#######################################OTP##############################################################################
@user.post("/send_otp", tags=["OTP"])
def send(user: User_basic, db: Session = Depends(get_db)):
    id = uuid.uuid4()
    output = send_otp(str(id), user, db)
    return output


@user.post("/verify_otp", tags=["OTP"])
def login(verifyotp: VerifyOtp, db: Session = Depends(get_db)):
    output = verify_otp(verifyotp, db)
    return output


##############################USERS###########################################################################################
@user.post("/create_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
def add_users(
    user: UserCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    uid = uuid.uuid4()
    output = add_user(
        str(uid),
        user.name,
        user.mobile,
        user.cc,
        user.dob,
        user.genderId,
        user.email,
        user.user_lat,
        user.user_long,
        user.country,
        user.state,
        user.district,
        user.locality,
        user.sub_locality,
        user.pincode,
        db,
    )
    return output


@user.post("/get_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
def get_users(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_user(str(user.uid), db, secure)
    return output


@user.get("/getUserByToken", tags=["User"])
def get_user_bytokens(
    db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = get_user_bytoken(secure, db)
    return output


@user.put("/update_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
def update_users(
    user: UpdateUser,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = update_user(
        str(user.uid),
        user.name,
        user.dob,
        user.genderId,
        user.email,
        user.user_lat,
        user.user_long,
        user.country,
        user.state,
        user.district,
        user.locality,
        user.sub_locality,
        user.pincode,
        db,
        secure,
    )
    return output


@user.delete("/delete_user", tags=["User"])
def delete_users(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_user(str(user.uid), db, secure)
    return output


@user.post("/userToSeller", tags=["User"])
def user_to_sellers(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = user_to_seller(str(user.uid), db, secure)
    return output


##############################STORES###########################################################################################
@user.post("/get_nearest_store", tags=["Store"])
def get_stores(
    store: UserLocation,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_loc(store.latitude, store.longitude, store.max_kms, db)
    return output


@user.post("/store/get_by_sellerId", tags=["Store"])
def get_stores_by_sellerids(
    store: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_sellerid(str(store.uid), db, secure)
    return output


@user.post("/store/get_nearest_by_category", tags=["Store"])
def get_stores_by_cats(
    store: StorebyCat,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_cat(
        str(store.categoryId), store.latitude, store.longitude, store.max_kms, db
    )
    return output


@user.post("/store/get_nearest_by_subcategory", tags=["Store"])
def get_stores_by_subcats(
    store: storebySubcat,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_stores_by_subcat(
        str(store.subcategoryId), store.latitude, store.longitude, store.max_kms, db
    )
    return output


@user.post("/stores/getStoreById", tags=["Store"])
def get_store_byIds(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_store_byId(str(store.storeId), db)
    return output


@user.post("/create_store", tags=["Store"])
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


@user.put("/update_store", tags=["Store"])
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


@user.delete("/delete_store", tags=["Store"])
def delete_stores(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_store(str(store.storeId), db, secure)
    return output


###########################################PRODUCTS##############################################################################
@user.post("/product/get_by_store_user", tags=["Product"])
def get_products_by_stores(
    product: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_store(str(product.storeId), db)
    return output


@user.post("/product/get_by_store_seller", tags=["Product"])
def get_products_by_store_sellers(
    product: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_store_seller(str(product.storeId), db, secure)
    return output


@user.post("/product/get_by_productId", tags=["Product"])
def get_products_by_id(
    product: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_product_by_id(str(product.productId), db)
    return output


@user.post("/product/get_by_categoryId", tags=["Product"])
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


@user.post("/product/toggleProductLiveStatus", tags=["Product"])
def toggleIsLives(
    product: IsLive,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = toggleIsLive(str(product.productId), product.isLive, db, secure)
    return output


@user.post("/create_product", tags=["Product"])
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


@user.put("/update_product", tags=["Product"])
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


@user.delete("/delete_product", tags=["Product"])
def delete_products(
    product: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_product(str(product.productId), db, secure)
    return output


@user.post("/get-searched-products", tags=["Product"])
def searchedProducts(
    body: SearchProduct,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getSearchedProducts(body, db, secure)
    print("output", output)
    return output


######################################VARIANTS##########################################################
@user.post("/getDetailedProductForUser", tags=["Product Variants"])
def get_variant_by_ids(
    variant: Product_id,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_variant_by_id(str(variant.productId), db)
    return output


@user.post("/getVariantListByProductId", tags=["Product Variants"])
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


@user.post("/create_variant", tags=["Product Variants"])
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


@user.put("/update_variant", tags=["Product Variants"])
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


@user.post("/get_varinat_images", tags=["Product Variants"])
def get_variant_images(
    variant: VariantImageD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_variant_image(variant.imageUrl, db)
    return output


@user.delete("/delete_variant", tags=["Product Variants"])
def delete_variants(
    variant: VariantID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_variant(str(variant.variantId), db)
    return output


@user.delete("/delete_variant_images", tags=["Product Variants"])
def delete_variant_images(
    variant: VariantImageD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_variant_image(variant.imageUrl, db)
    return output


@user.delete("/delete_variant_size", tags=["Product Variants"])
def delete_variant_sizes(
    size: SqpD, db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = delete_variant_size(str(size.sqpId), db)
    return output


######################################Transactions###############################################################
@user.post("/get_transactions_by_userId", tags=["Transactions"])
def get_transacitons(
    transaction: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_transaction(str(transaction.uid), db, secure)
    return output


@user.post("/create_transaction", tags=["Transactions"])
def post_transactions(
    transaction: TransactionC,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    transactionId = uuid.uuid4()
    output = post_transaction(
        str(transactionId),
        str(transaction.uid),
        str(transaction.productId),
        transaction.description,
        transaction.razorpayPaymentId,
        transaction.added,
        transaction.credits_3m,
        transaction.credits_6m,
        transaction.credits_12m,
        transaction.totalCredits,
        transaction.cost_3m,
        transaction.cost_6m,
        transaction.cost_12m,
        transaction.totalCost,
        transaction.discount,
        transaction.grandTotal,
        transaction.couponId,
        db,
        secure,
    )
    return output


@user.get("/get_couponCodes", tags=["Transactions"])
def get_couponCodes(
    db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = get_couponCode(db)
    return output


@user.post("/getCreditBalance", tags=["Transactions"])
def getCreditBalances(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getCreditBalance(str(user.uid), db, secure)
    return output


########################################Filters#################################################################################
@user.post("/filter_variants", tags=["Filters"])
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


@user.post("/scope_of_store_filters", tags=["Filters"])
def scope_stores(
    storeCat: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = scope_store(str(storeCat.storeId), str(storeCat.categoryId), db)
    return output


@user.post("/scope_of_store_filters_modified", tags=["Filters"])
def scope_stores_modifieds(
    storeCat: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = scope_store_modified(str(storeCat.storeId), str(storeCat.categoryId), db)
    return output


@user.post("/brand_in_store", tags=["Filters"])
def get_brands(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_brand(str(store.storeId), db)
    return output


@user.post("/category_in_store", tags=["Filters"])
def get_categories(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_category(str(store.storeId), db)
    return output


@user.post("/subcategory_in_store", tags=["Filters"])
def get_categories(
    store: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_sub_category(str(store.storeId), str(store.categoryId), db)
    return output


@user.post("/size_in_store", tags=["Filters"])
def get_sizes(
    store: StoreCatId,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_size(str(store.storeId), str(store.categoryId), db)
    return output


@user.post("/material_in_store", tags=["Filters"])
def get_materials(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_material(str(store.storeId), db)
    return output


@user.post("/color_in_store", tags=["Filters"])
def get_colors(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_color(str(store.storeId), db)
    return output


@user.post("/price_in_store", tags=["Filters"])
def get_prices(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_maxprice(str(store.storeId), db)
    return output


@user.post("/gender_in_store", tags=["Filters"])
def get_genders(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_gender(str(store.storeId), db)
    return output


@user.post("/country_in_store", tags=["Filters"])
def get_countries(
    store: StoreID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_country(str(store.storeId), db)
    return output


# @user.get('/get_cgender', tags=['testtt'])
# def get_couponCodes(db:Session=Depends(get_db)):#, secure=Depends(auth_handler.auth_wrapper)):
#     output = db.query(models.Brand).filter(models.Brand.is_custom).all()
#     return output

# @user.get('/put_gendef', tags=['testtt'])
# def get_couponCodes(something, is_custom ,db:Session=Depends(get_db)):#, secure=Depends(auth_handler.auth_wrapper)):
#     output = models.TEst(something=something, is_custom=is_custom)
#     db.add(output)
#     db.commit()
#     return output


#################################################GET ATTRIBUTES##################################################
@user.post("/get-all-brands", tags=["Attributes"])
def get_brands(
    body: BrandNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return get_all_brands(body.brandNames, db)


@user.post("/getSubcategoryByCategory", tags=["Attributes"])
def get_subcat_by_cats(
    cat: CategoryIDD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_subcat_by_cat(cat.subCategoryNames, str(cat.categoryId), db)
    return output


@user.post("/getAllCategories", tags=["Attributes"])
def getAllCategories(
    body: CategoryNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllcategory(db, body.categoryNames)
    return output


@user.post("/getAllSizes", tags=["Attributes"])
def getAllSizes(
    size: GetSizes,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllSize(
        size.sizeNames, str(size.categoryId), str(size.subcategoryId), db
    )
    return output


@user.post("/getAllMaterials", tags=["Attributes"])
def getAllMaterials(
    body: MaterialNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllMaterial(body.materialNames, db)
    return output


@user.post("/getAllColors", tags=["Attributes"])
def getAllColors(
    body: ColorNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllColor(body.colorNames, db)
    return output


@user.post("/getAllCountries", tags=["Attributes"])
def getAllCountries(
    body: CountryNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllCountry(body.countryNames, db)
    return output


@user.post("/getAllGenders", tags=["Attributes"])
def getAllGenders(
    body: GenderNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllgender(body.genderNames, db)
    return output


########################################bulk upload###################################################


@user.post("/bulk-upload/products", tags=["Bulk Uploads"])
def bulkUploadProducts(
    body: BulkUploadProductCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return bulkUploadProduct(body, db, secure)


@user.post("/bulk-upload/variants", tags=["Bulk Uploads"])
def bulkUploadVariants(
    body: BulkUploadVariantCreate,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return bulkUploadVariant(body, db)
