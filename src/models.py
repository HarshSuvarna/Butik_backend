from database import Base
from sqlalchemy import VARCHAR, Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, VARCHAR, Float, Boolean

class Users(Base):
    __tablename__ = 'userdetails'

    uid = Column(VARCHAR(50), primary_key=True, index=True)
    mobile = Column(String(20))
    cc = Column(String(20))
    name = Column(String(50))
    threeMonthsCredits = Column(Integer)
    sixMonthsCredits = Column(Integer)
    twelveMonthsCredits = Column(Integer)
    dob = Column(String(50))
    genderId = Column(Integer,ForeignKey('gender.genderId'))
    email = Column(String(50))
    isSeller = Column(Boolean)  
    logged_in = Column(String(50))
    is_deleted = Column(String(50))
    creationTime = Column(String(50))
    last_updated = Column(String(50))
    
    stores = relationship('CreateStore', backref='user')
    locations = relationship('UserLocations', backref='user')
    products = relationship('Products', backref='user')
    transactions = relationship('Transactions', backref='user')
   

class UserLocations(Base):

    __tablename__= 'userlocation'
    index = Column(Integer, primary_key=True, index=True)
    uid = Column(VARCHAR(50),ForeignKey('userdetails.uid'))
    user_long = Column(String(50)) 
    user_lat = Column(String(50))
    country = Column(String(30))
    state= Column(String(50))
    district= Column(String(50))
    locality= Column(String(50))
    sub_locality= Column(String(50))
    pincode = Column(String(10))

class CreateStore(Base):

    __tablename__ = 'stores'

    storeId = Column(VARCHAR(50), primary_key=True, index=True)
    uid = Column(VARCHAR(50), ForeignKey('userdetails.uid'))
    storeName = Column(String(80))
    wholeSellerOrRetailer = Column(String(50))
    storePhone = Column(String(20))
    store_add_1 = Column(String(100))
    store_add_2 = Column(String(100))
    landmark = Column(String(80))
    longitude = Column(Float)
    latitude = Column(Float)
    country = Column(String(30))
    state = Column(String(50))
    district = Column(String(50))
    locality = Column(String(50))
    subLocality = Column(String(50))
    pinCode = Column(String(15))
    gst = Column(String(50))
    pan = Column(String(50))
    is_deleted = Column(String(50))
    status = Column(String(50))
    created_on = Column(String(50))
    last_updated = Column(String(50))
    storeImageURL = Column(String(600))
    
    products = relationship('Products', backref= 'store')
    variant_size_prices = relationship('VariantSizePrice', backref='store')
    variants = relationship('ProductVariant', backref='store')
    variant_images = relationship('VariantImages', backref='store')



class OTPs(Base):

    __tablename__ = 'otp_table'
    otp_id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer)
    mobile = Column(String(50))
    cc = Column(String(50))
    otp_code = Column(String(50))
    created_on = Column(String(50))
    status = Column(String(50))
    otp_failed_count = Column(Integer)
    expiration_time = Column(String(50))



class Products(Base):

    __tablename__ = 'products'

    productId = Column(VARCHAR(50), primary_key=True, index=True)
    productName = Column(String(40)) 
    productDescription = Column(String(255))
    categoryId = Column(Integer,ForeignKey('product_category.categoryId'))
    brandId = Column(Integer, ForeignKey('brands.brandId'))
    materialId = Column(Integer, ForeignKey('material.materialId'))
    storeId = Column(VARCHAR(50), ForeignKey('stores.storeId'))
    uid = Column(VARCHAR(50), ForeignKey('userdetails.uid'))
    subCategoryId = Column(Integer, ForeignKey('product_subcategory.subcategoryId'))
    genderId = Column(Integer, ForeignKey('gender.genderId')) 
    country_id = Column(Integer, ForeignKey('country.countryId')) 
    imagesUrl = Column(String(600))
    is_deleted = Column(String(40)) 
    isLive = Column(Boolean)
    expiry = Column(String(40)) 
    created_on = Column(String(40)) 
    updated_on = Column(String(40)) 

    product_variants = relationship('ProductVariant', backref='product')
    variant_size_prices = relationship('VariantSizePrice', backref='product')
    variant_images = relationship('VariantImages', backref='product')
    transactions = relationship('Transactions', backref='products')

class ProductVariant(Base):
    __tablename__ = 'product_variants'
    variantId = Column(VARCHAR(50), primary_key=True, index=True)
    productId = Column(VARCHAR(50), ForeignKey('products.productId'))
    storeId = Column(VARCHAR(50), ForeignKey('stores.storeId'))
    colorId = Column(Integer, ForeignKey('color.colorId'))
    created_on = Column(String(50))
    is_deleted = Column(String(40)) 
    is_visible = Column(String(40))
    updated_on = Column(String(50)) 

    variant_size_prices = relationship('VariantSizePrice', backref='variant')
    variant_images = relationship('VariantImages', backref='variant')
    

class Transactions(Base):

    __tablename__ = 'transaction'
    transactionId = Column(VARCHAR(50), primary_key=True, index=True)
    uid = Column(VARCHAR(50), ForeignKey('userdetails.uid'))
    productId = Column(VARCHAR(50), ForeignKey('products.productId'))
    description = Column(String(255))
    credits_3m = Column(Integer)
    credits_6m = Column(Integer)
    credits_12m = Column(Integer)
    totalCredits = Column(Integer)
    cost_3m = Column(Float)
    cost_6m = Column(Float)
    cost_12m = Column(Float)
    totalCost = Column(Float)
    discount = Column(Float)
    grandTotal = Column(Float)
    couponId = Column(Integer, ForeignKey('coupons.couponId'))
    razorpayPaymentId = Column(String(20))
    added = Column(Integer)
    transactionDate =  Column(String(50))


class CouponS(Base):
    
    __tablename__ = 'coupons'
    couponId = Column(Integer, primary_key=True, index=True)
    couponCode = Column(String(40))

    transactions = relationship('Transactions', backref='coupon')


class VariantImages(Base):
    __tablename__ = 'product_variant_images'
    image_id = Column(Integer, primary_key=True, index=True)
    variantId = Column(VARCHAR(50), ForeignKey('product_variants.variantId'))
    productId = Column(VARCHAR(50), ForeignKey('products.productId'))
    storeId = Column(VARCHAR(50), ForeignKey('stores.storeId'))
    image_url = Column(String(600))


class VariantSizePrice(Base):
    __tablename__ = 'variant_size_price'
    spqId = Column(Integer, primary_key=True, index=True)
    storeId = Column(VARCHAR(50), ForeignKey('stores.storeId'))
    productId = Column(VARCHAR(50), ForeignKey('products.productId'))
    variantId = Column(VARCHAR(50), ForeignKey('product_variants.variantId'))
    sizeId = Column(Integer, ForeignKey('size.sizeId'))
    price = Column(Integer)
    quantity = Column(Integer)


class Brand(Base):
    __tablename__ = 'brands'
    brandId = Column(Integer, primary_key=True, index=True)
    brandName = Column(String(50))
    categoryId = Column(Integer, ForeignKey('product_category.categoryId'))

    products = relationship('Products', backref='brand')

class Categories(Base):
    __tablename__ = 'product_category'
    categoryId = Column(Integer, primary_key=True, index=True)
    categoryName = Column(String(50))
    icon = Column(String(200))

    products = relationship('Products', backref='category')
    subcategories = relationship('SubCategories', backref='category')
    sizes = relationship('Sizes', backref='category')
    brands = relationship('Brand', backref='category')

class SubCategories(Base):
    __tablename__ = 'product_subcategory'
    subcategoryId = Column(Integer, primary_key=True, index=True)
    subcategoryName = Column(String(50))
    description = Column(String(255))
    categoryId = Column(Integer, ForeignKey('product_category.categoryId'))
    
    products = relationship('Products', backref='subcategory')
    sizes = relationship('Sizes', backref='subcategory')

class Sizes(Base):
    __tablename__ = 'size'
    sizeId = Column(Integer, primary_key=True, index=True)
    size = Column(String(10))
    categoryId = Column(Integer, ForeignKey('product_category.categoryId'))
    subcategoryId = Column(Integer, ForeignKey('product_subcategory.subcategoryId'))

    variant_size_prices = relationship('VariantSizePrice', backref='size')

class Materials(Base):
    __tablename__ = 'material'
    materialId = Column(Integer, primary_key=True, index=True)
    material = Column(String(50))
    
    products = relationship('Products', backref='material')

class Colors(Base):
    __tablename__ = 'color'
    colorId = Column(Integer, primary_key=True, index=True)
    color = Column(String(50))
    
    product_vars = relationship('ProductVariant', backref='color')
    
class Countries(Base):
    __tablename__ = 'country'
    countryId = Column(Integer, primary_key=True, index=True)
    country = Column(String(50))

    products = relationship('Products', backref='country')
    
class Genders(Base):
    __tablename__ = 'gender'
    genderId = Column(Integer, primary_key=True, index=True)
    gender = Column(String(30))

    users = relationship('Users', backref='gender')
    products = relationship('Products', backref='gender')

class TEst(Base):
    __tablename__='testt'
    testId = Column(Integer, primary_key=True, index=True)
    something =Column(String(50))
    is_custom = Column(Boolean)