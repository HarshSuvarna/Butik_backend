from src.db.models import CreateStore, Genders, Products, Categories, SubCategories, Brand, Colors, Materials, \
VariantSizePrice, Sizes, ProductVariant, Countries
from sqlalchemy import func


def scope_store(storeId, categoryId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        cat_qs= db.query(Products.categoryId, Categories.categoryName.label('categoryName'))\
                  .distinct(Products.categoryId)\
                  .join(Categories, Categories.categoryId==Products.categoryId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                  .all()

        subcat_q= db.query(Products.subCategoryId, SubCategories.subcategoryName.label('subcategoryName'))\
                    .distinct(Products.subCategoryId)\
                    .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                    .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                    .all()

        size_q= db.query(VariantSizePrice.sizeId, Sizes.size).distinct(VariantSizePrice.sizeId)\
                  .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                  .join(Products, Products.productId==VariantSizePrice.productId)\
                  .filter(VariantSizePrice.storeId==storeId, Products.categoryId==categoryId)\
                  .distinct(VariantSizePrice.sizeId)\
                  .all()

        color_q= db.query(ProductVariant.colorId, Colors.color).distinct(ProductVariant.colorId)\
                  .join(Colors, Colors.colorId==ProductVariant.colorId)\
                  .join(Products, Products.productId==ProductVariant.productId)\
                  .filter(ProductVariant.storeId==storeId, Products.categoryId==categoryId)\
                  .all()

        gender_q= db.query(Products.genderId, Genders.gender).distinct(Products.genderId)\
                  .join(Genders, Genders.genderId==Products.genderId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                  .all()

        material_q= db.query(Products.materialId, Materials.material.label('Material')).distinct(Products.materialId)\
                  .join(Materials, Materials.materialId==Products.materialId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                  .all()

        brand_q = db.query(Products.brandId, Brand.brandName)\
                .distinct(Products.brandId)\
                .join(Brand, Brand.brandId==Products.brandId)\
                .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                .all()

        country_q= db.query(Products.country_id, Countries.country)\
                   .distinct(Products.country_id)\
                   .join(Countries, Countries.countryId==Products.country_id)\
                   .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                   .all()

        price_q= db.query(func.max(VariantSizePrice.price))\
                   .join(Products, Products.productId==VariantSizePrice.productId)\
                   .filter(VariantSizePrice.storeId==storeId, Products.categoryId==categoryId)\
                   .all()
        
        attListName = {'categoryFilter':cat_qs, 
                       'subcategoryFilter':subcat_q, 
                       'sizeFilter':size_q, 
                       'colorFilter':color_q, 
                       'brandFilter':brand_q, 
                       'materialFilter':material_q, 
                       'genderFilter':gender_q, 
                       'maxPrice':price_q[0][0], 
                       'countryFilter':country_q}

        #print('max Price=>',price_q)
        return {'status_code':200, 'message':'success','data':attListName}

def scope_store_modified(storeId, categoryId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        cat_qs= db.query(Products.categoryId.label('id'), Categories.categoryName.label('name'))\
                  .distinct(Products.categoryId)\
                  .join(Categories, Categories.categoryId==Products.categoryId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                  .all()

        subcat_q= db.query(Products.subCategoryId.label('id'), SubCategories.subcategoryName.label('name'))\
                    .distinct(Products.subCategoryId)\
                    .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                    .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                    .all()

        size_q= db.query(VariantSizePrice.sizeId.label('id'), Sizes.size.label('name')).distinct(VariantSizePrice.sizeId)\
                  .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                  .join(Products, Products.productId==VariantSizePrice.productId)\
                  .filter(VariantSizePrice.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                  .distinct(VariantSizePrice.sizeId)\
                  .all()

        color_q= db.query(ProductVariant.colorId.label('id'), Colors.color.label('name')).distinct(ProductVariant.colorId)\
                  .join(Colors, Colors.colorId==ProductVariant.colorId)\
                  .join(Products, Products.productId==ProductVariant.productId)\
                  .filter(ProductVariant.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                  .all()

        gender_q= db.query(Products.genderId.label('id'), Genders.gender.label('name')).distinct(Products.genderId)\
                  .join(Genders, Genders.genderId==Products.genderId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                  .all()

        material_q= db.query(Products.materialId.label('id'), Materials.material.label('name')).distinct(Products.materialId)\
                  .join(Materials, Materials.materialId==Products.materialId)\
                  .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                  .all()

        brand_q = db.query(Products.brandId.label('id'), Brand.brandName.label('name'))\
                    .distinct(Products.brandId)\
                    .join(Brand, Brand.brandId==Products.brandId)\
                    .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                    .all()

        country_q= db.query(Products.country_id.label('id'), Countries.country.label('name'))\
                   .distinct(Products.country_id)\
                   .join(Countries, Countries.countryId==Products.country_id)\
                   .filter(Products.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                   .all()

        price_q= db.query(func.max(VariantSizePrice.price))\
                   .join(Products, Products.productId==VariantSizePrice.productId)\
                   .filter(VariantSizePrice.storeId==storeId, Products.categoryId==categoryId, Products.isLive==1)\
                   .all()
        
        attListName = {'categoryFilter':cat_qs, 
                       'subcategoryFilter':subcat_q, 
                       'sizeFilter':size_q, 
                       'colorFilter':color_q, 
                       'brandFilter':brand_q, 
                       'materialFilter':material_q, 
                       'genderFilter':gender_q, 
                       'maxPrice':price_q[0][0], 
                       'countryFilter':country_q}

        #print('max Price=>',price_q)
        return {'status_code':200, 'message':'success','data':attListName}


def get_category(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        cat_qs= db.query(Products.categoryId, Categories.categoryName.label('categoryName'))\
                  .distinct(Products.categoryId)\
                  .join(Categories, Categories.categoryId==Products.categoryId)\
                  .filter(Products.storeId==storeId, Products.isLive==1)\
                  .all()

        if cat_qs ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(cat_qs))+' results found','data':cat_qs}

def get_sub_category(storeId, categoryId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        subcat_q= db.query(Products.subCategoryId, SubCategories.subcategoryName.label('subcategoryName'))\
                    .distinct(Products.subCategoryId)\
                    .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                    .filter(Products.storeId==storeId, Products.categoryId==categoryId)\
                    .all()
        
        if subcat_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(subcat_q))+' results found', 'data':subcat_q}
        

def get_size(storeId, categoryId , db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        size_q= db.query(VariantSizePrice.sizeId, Sizes.size).distinct(VariantSizePrice.sizeId)\
                  .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                  .join(Products, Products.productId==VariantSizePrice.productId)\
                  .filter(VariantSizePrice.storeId==storeId, Products.categoryId==categoryId)\
                  .distinct(VariantSizePrice.sizeId)\
                  .all()

        if size_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(size_q))+' results found', 'data':size_q}

def get_color(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        color_q= db.query(ProductVariant.colorId, Colors.color).distinct(ProductVariant.colorId)\
                  .join(Colors, Colors.colorId==ProductVariant.colorId)\
                  .filter(ProductVariant.storeId==storeId)\
                  .all()
        if color_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(color_q))+' results found', 'data':color_q}

def get_gender(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        gender_q= db.query(Products.genderId, Genders.gender).distinct(Products.genderId)\
                  .join(Genders, Genders.genderId==Products.genderId)\
                  .filter(Products.storeId==storeId)\
                  .all()
        if gender_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(gender_q))+' results found','data':gender_q}



def get_material(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        material_q= db.query(Products.materialId, Materials.material.label('Material')).distinct(Products.materialId)\
                  .join(Materials, Materials.materialId==Products.materialId)\
                  .filter(Products.storeId==storeId)\
                  .all()
        if material_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(material_q))+' results found','data':material_q}


def get_brand(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
   #print('store=>',store_q)
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
       #print('in Elsessssessss')
        brand_q = db.query(Products.brandId, Brand.brandName)\
                    .distinct(Products.brandId)\
                    .join(Brand, Brand.brandId==Products.brandId)\
                    .filter(Products.storeId==storeId)\
                    .all()
        if brand_q ==None:
           #print('in IFFFFFF')
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
           #print('insendocn else')
            return {'status_code':200, 'message':str(len(brand_q))+' brands found','data':brand_q}

def get_maxprice(storeId, db):
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        price_q= db.query(func.max(VariantSizePrice.price))\
                   .filter(VariantSizePrice.storeId==storeId)\
                   .all()
       #print(price_q)
        if len(price_q) ==0:
           return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':'results found', 'data':price_q[0][0]}


def get_country(storeId, db):
    
    store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
    
    if store_q==None:
        return {'status_code':0, 'message':'invalid store', 'data':{}}
    else:
        country_q= db.query(Products.country_id, Countries.country)\
                   .distinct(Products.country_id)\
                   .join(Countries, Countries.countryId==Products.country_id)\
                   .filter(Products.storeId==storeId)\
                   .all()
        if country_q ==None:
            return {'status_code':0, 'message':'No results found', 'data':{}}
        else:
            return {'status_code':200, 'message':str(len(country_q))+' results found','data':country_q}