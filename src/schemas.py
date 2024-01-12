from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional, List


class User_basic(BaseModel):
    cc: str = Field(max_length=5, min_length=2)
    mobile: str = Field(max_length=10, min_length=10)


class VerifyOtp(User_basic):
    otp: str = Field(max_length=6)
    otp_for: str


class UserCreate(BaseModel):
    name: Optional[str] = None
    mobile: str = Field(max_length=10, min_length=10)
    cc: str = Field(max_length=3)
    dob: Optional[str] = None
    genderId: Optional[int] = None
    email: Optional[str] = None
    user_lat: Optional[float]
    user_long: Optional[float]
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    locality: Optional[str] = None
    sub_locality: Optional[str] = None
    pincode: Optional[str] = None


class UpdateUser(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str = Field(..., max_length=50)
    dob: str = Field(..., max_length=10)
    genderId: int
    email: str
    user_lat: Optional[float] = None
    user_long: Optional[float] = None
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    locality: Optional[str] = None
    sub_locality: Optional[str] = None
    pincode: Optional[str] = None


class UserID(BaseModel):
    uid: UUID = Field(default_factory=uuid4)


class StoreID(BaseModel):
    storeId: UUID = Field(default_factory=uuid4)


class StoreCatId(BaseModel):
    storeId: UUID = Field(default_factory=uuid4)
    categoryId: int


class ProductFilter(BaseModel):
    storeId: List[str]
    colorId: List[int]
    brandId: List[int]
    sizeId: List[int]
    materialId: List[int]
    categoryId: List[int]
    subcategoryId: List[int]
    genderId: List[int]
    maxPrice: List[int]


class CountryID(BaseModel):
    countryId: int


class StoreCreate(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    storeName: str
    wholeSellerOrRetailer: str
    storeImageURL: str
    storePhone: str
    store_add_1: str
    store_add_2: str
    landmark: str
    longitude: float
    latitude: float
    country: str
    state: str
    district: str
    locality: Optional[str] = None
    subLocality: Optional[str] = None
    pinCode: str
    gst: Optional[str] = None  # Field(None,max_length=15, min_length=15)
    pan: Optional[str] = None  # Field(None,max_length=10, min_length=10)
    status: Optional[str] = None


class StoreU(StoreID):
    storeName: str
    wholeSellerOrRetailer: str
    storeImageURL: str
    storePhone: str
    store_add_1: str
    store_add_2: str
    landmark: str
    longitude: float
    latitude: float
    country: str
    state: str
    district: str
    locality: Optional[str] = None
    subLocality: Optional[str] = None
    pinCode: str
    gst: Optional[str] = None  # =Field(None,max_length=15, min_length=15)
    pan: Optional[str] = None  # =Field(None,max_length=10, min_length=10)
    status: str


class TransactionC(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    productId: UUID = None
    description: Optional[str] = None
    credits_3m: Optional[int] = None
    credits_6m: Optional[int] = None
    credits_12m: Optional[int] = None
    totalCredits: Optional[int] = None
    cost_3m: Optional[float] = None
    cost_6m: Optional[float] = None
    cost_12m: Optional[float] = None
    totalCost: Optional[float] = None
    discount: Optional[float] = None
    grandTotal: Optional[float] = None
    couponId: Optional[int] = None
    razorpayPaymentId: Optional[str] = None
    added: bool


class TransactionID(BaseModel):
    transactionId: UUID = Field(default_factory=uuid4)


class UserLocation(BaseModel):
    latitude: float
    longitude: float
    max_kms: int


class StorebyCat(UserLocation):
    categoryId: int


class storebySubcat(UserLocation):
    subcategoryId: int


class ProductCreate(BaseModel):
    productName: str
    productDescription: str
    categoryId: int
    brandId: int
    materialId: int
    storeId: UUID = Field(default_factory=uuid4)
    uid: UUID = Field(default_factory=uuid4)
    subCategoryId: int
    genderId: int
    countryId: int
    productImageUrl: Optional[str] = None
    planName: Optional[str] = None


class ProductBulkUpload(ProductCreate):
    productId: UUID = None


class BulkUploadProductCreate(BaseModel):
    products: List[dict]


class ProductU(BaseModel):
    productId: UUID = Field(default_factory=uuid4)
    productName: str
    productDescription: str
    categoryId: int
    brandId: int
    materialId: int
    storeId: UUID = Field(default_factory=uuid4)
    uid: UUID = Field(default_factory=uuid4)
    subCategoryId: int
    genderId: int
    countryId: int
    productImageUrl: Optional[str] = None
    isLive: bool


class Product_id(BaseModel):
    productId: UUID = Field(default_factory=uuid4)


class IsLive(Product_id):
    isLive: bool


class VariantCreate(BaseModel):
    productId: UUID = Field(default_factory=uuid4)
    storeId: UUID = Field(default_factory=uuid4)
    colorId: int
    imagesUrlList: Optional[List[str]] = None
    spqList: List[dict]


class SearchProduct(BaseModel):
    searchedProduct: str = Field(..., min_length=2)
    latitude: float
    longitude: float


class BulkUploadVariantCreate(BaseModel):
    variants: List[VariantCreate]


class CategoryID(UserLocation):
    categoryId: int


class VariantUpdate(BaseModel):
    variantId: UUID = Field(default_factory=uuid4)
    productId: UUID = Field(default_factory=uuid4)
    storeId: UUID = Field(default_factory=uuid4)
    colorId: int
    imagesUrlList: Optional[List[str]] = None
    spqList: List[dict]


class VariantID(BaseModel):
    variantId: UUID = Field(default_factory=uuid4)


class VariantImageD(BaseModel):
    imageUrl: str


class SqpD(BaseModel):
    sqpId: int


class VariantG(BaseModel):
    pass


class CategoryIDD(BaseModel):
    categoryId: Optional[int] = None
    subCategoryNames: Optional[List[str]] = None


class BrandNames(BaseModel):
    brandNames: Optional[List[str]] = None


class CategoryNames(BaseModel):
    categoryNames: Optional[List[str]] = None


class MaterialNames(BaseModel):
    materialNames: Optional[List[str]] = None


class ColorNames(BaseModel):
    colorNames: Optional[List[str]] = None


class CountryNames(BaseModel):
    countryNames: Optional[List[str]] = None


class GenderNames(BaseModel):
    genderNames: Optional[List[str]] = None


class GetSizes(BaseModel):
    categoryId: Optional[int] = None
    subcategoryId: Optional[int] = None
    sizeNames: Optional[List[str]] = None
