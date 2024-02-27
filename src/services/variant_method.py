from src.db.models import Brand, Categories, CreateStore, Materials, Products, Sizes, ProductVariant, SubCategories, VariantSizePrice, VariantImages, Colors
from datetime import datetime, timedelta
from src.schemas import VariantCreate
from src.helper.upload_image import uploadToBucket_variants, deleteVariantImgs

def add_variant(variantId, productId, storeId, colorId, spqList, imagesUrlList,db):
        
   
        product_q = db.query(Products).filter(Products.productId==productId).first()
        store_q = db.query(CreateStore).filter(CreateStore.storeId==storeId).first()
        if product_q==None:
            return {'status_code':0,'message':'product id not valid', 'data':{}}
        elif store_q==None:
            return {'status_code':0,'message':'store id not valid', 'data':{}}
        else:
            
            productvar_q = ProductVariant(variantId=variantId ,productId= productId, colorId=colorId, storeId=storeId, is_deleted=0, is_visible=1, 
                                          created_on=datetime.now().replace(microsecond=0))
            db.add(productvar_q)
            db.commit()
                
            variant_q = db.query(ProductVariant)\
                          .filter(ProductVariant.variantId==variantId)\
                          .first()
            for i in range(len(spqList)):
                size_q = db.query(Sizes).filter(Sizes.sizeId==spqList[i]['sizeId']).first()
                variant_sp_q = VariantSizePrice(productId=productId, size=size_q, storeId=storeId, variant=variant_q, price=spqList[i]['price'], 
                                                quantity=spqList[i]['quantity'])
                db.add(variant_sp_q)
                db.commit()
            imgUrlL = []
            for i in range(len(imagesUrlList)):
                img_url = uploadToBucket_variants(variantId, i, imagesUrlList[i])
                var_img_q = VariantImages(variant=variant_q, productId=productId, storeId=storeId, image_url=img_url)
                db.add(var_img_q)
                db.commit()
                imgUrlL.append(img_url)
            return {'status_code':200, 'message':'variant created successfully', 'data':{'productId':productId,'variantId':variantId, 'productId':productId, 
                    'storeId':storeId, 'colorId':colorId, 'spqList':spqList, 'imagesUrlList':imgUrlL}}

def update_variant(variantId, productId, storeId, colorId, spqList, imagesUrlList,db):
    
    variant_q= db.query(ProductVariant).filter(ProductVariant.variantId==variantId, ProductVariant.is_deleted==0).first()
    if variant_q==None:
        return {'status_code':0,'message':'Variant doesnt exist', 'data':{}}
    else:
        variants_q = db.query(ProductVariant).filter(ProductVariant.variantId == variantId).update({ProductVariant.storeId:storeId ,ProductVariant.colorId:colorId , ProductVariant.productId:productId, ProductVariant.updated_on:datetime.now().replace(microsecond=0)})
        db.commit()
        variant_del = db.query(VariantSizePrice).filter(VariantSizePrice.variantId==variantId).delete(synchronize_session=False)
        db.commit()
        var_image_del =db.query(VariantImages).filter(VariantImages.variantId==variantId).delete(synchronize_session=False)
        variant_q = db.query(ProductVariant).filter(ProductVariant.productId==productId, ProductVariant.storeId==storeId, ProductVariant.colorId==colorId).first()
        for i in range(len(spqList)):
            size_q = db.query(Sizes).filter(Sizes.sizeId==spqList[i]['sizeId']).first()
            variant_sp_q = VariantSizePrice(productId=productId, size=size_q, storeId=storeId, variant=variant_q, price=spqList[i]['price'], quantity=spqList[i]['quantity'])
            db.add(variant_sp_q)
            db.commit()
        imgUrlL=[]
        if imagesUrlList:
            for i in range(len(imagesUrlList)):
                if len(imagesUrlList[i])>=90:
                    img_url = uploadToBucket_variants(variantId, i, imagesUrlList[i])
                else:
                    img_url = imagesUrlList[i]
                var_img_q = VariantImages(variant=variant_q, productId=productId, storeId=storeId, image_url=img_url)
                db.add(var_img_q)
                db.commit()
                imgUrlL.append(img_url)
        return {'status_code':200,'message':'variant updated successfully', 'data':{'productId':productId,'variantId':variantId, 'productId':productId, 'storeId':storeId, 'colorId':colorId, 'spqList':spqList, 'imagesUrlList':imgUrlL}}


def delete_variant_image(imageUrl, db):
    image_q  = db.query(VariantImages.variantId).filter(VariantImages.image_url==imageUrl).first()
    if image_q ==None:
        return {'status_code':0,'message':'Image does not exist', 'data':{}}
    else:
        image_d = db.query(VariantImages).filter(VariantImages.image_url==imageUrl).delete(synchronize_session=False)
        db.commit()
        deleteVariantImgs(image_q[0],1)
        return {'status_code':200, 'message': 'Image Deleted Successfully', 'data':{}}
        

def delete_variant_size(sqpId, db):
    size_q  = db.query(VariantSizePrice.spqId).filter(VariantSizePrice.spqId==sqpId).first()
    if size_q ==None:
        return {'status_code':0,'message':'Size does not exist', 'data':{}}
    else:
        size_d = db.query(VariantSizePrice).filter(VariantSizePrice.spqId==sqpId).delete(synchronize_session=False)
        db.commit()
        return {'status_code':200, 'message': 'SPQ Deleted Successfully', 'data':{'spqId':sqpId, 'variantId':size_q[0]}}
        
def delete_variant(variantId, db):
    var_q  = db.query(ProductVariant.variantId).filter(ProductVariant.variantId==variantId).first()
    if var_q ==None:
        return {'status_code':0,'message':'Variant does not exist', 'data':{}}
    else:
        size_d = db.query(VariantSizePrice).filter(VariantSizePrice.variantId==variantId).delete(synchronize_session=False)
        db.commit()
        image_ds = db.query(VariantImages).filter(VariantImages.variantId==variantId).all()
        image_d = db.query(VariantImages).filter(VariantImages.variantId==variantId).delete(synchronize_session=False)
        db.commit()
        var_d = db.query(ProductVariant).filter(ProductVariant.variantId==variantId).delete(synchronize_session=False)
        db.commit()
        deleteVariantImgs(variantId, len(image_ds))
        return {'status_code':200, 'message': 'Variant Deleted Successfully', 'data':{'VariantID':variantId}}

def get_variant_image(variantId, db):
    image_q  = db.query(VariantImages.image_url).filter(VariantImages.variantId==variantId).all()
    if len(image_q) ==0:
        return {'status_code':0,'message':'Image does not exist', 'data':[]}
    else:
        imageList=[]
        for i in range(len(image_q)):
            imageList.append(image_q[i][0])
        return {'status_code':200, 'message': str(len(imageList))+' results found', 'data':imageList}

def get_variant_by_id(productId, db):
    product_q = db.query(ProductVariant).filter(ProductVariant.productId==productId).first()
    if product_q==None:
        return {'status_code':200, 'message':'product does not exist','data':{}}
    else:
        product_q = db.query(ProductVariant.variantId, Products.productName,Categories.categoryName, Colors.color, Materials.material, ProductVariant.storeId, Products.productDescription, Brand.brandName, Products.imagesUrl, SubCategories.subcategoryName, Products.productId)\
                      .join(Products, Products.productId==ProductVariant.productId)\
                      .join(Categories, Categories.categoryId==Products.categoryId)\
                      .join(Colors, Colors.colorId==ProductVariant.colorId)\
                      .join(Materials, Materials.materialId==Products.materialId)\
                      .join(Brand, Brand.brandId==Products.brandId)\
                      .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                      .filter(Products.productId==productId).all()
        
        store_q = db.query(CreateStore.storeId, CreateStore.storeName, CreateStore.locality, CreateStore.district, CreateStore.storePhone, CreateStore.latitude, CreateStore.longitude).filter(CreateStore.storeId==product_q[0][5]).all()
        
        store_att= ['storeId','storeName','locality', 'district', 'storePhone','latitude', 'longitude']
        spq_att = ['spqId','size', 'sizeId','price', 'quantity']
        outputList = []
        images=[]
        sizes = []
        dataJson={}
        for i in range(len(product_q)):
            size_q = db.query(VariantSizePrice.spqId, Sizes.size, Sizes.sizeId, VariantSizePrice.price, VariantSizePrice.quantity, VariantSizePrice.variantId)\
                        .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                        .filter(VariantSizePrice.variantId==product_q[i][0])\
                        .all()
            image_q = db.query(VariantImages.image_id, VariantImages.image_url)\
                        .filter(VariantImages.variantId==product_q[i][0])\
                        .order_by(VariantImages.variantId)\
                        .all()
            images=[]
            sizes = []
            for size in size_q:
                sizes.append(dict(zip(spq_att, size)))
                
            for image in image_q:
                images.append(image[1])

            variant_json = {"variantId":product_q[i][0], "categoryName":product_q[i][2], "color":product_q[i][3], "spqList":sizes, "imagesUrlList":images}
            outputList.append(variant_json)
        dataJson['variantList'] = outputList
        dataJson['seller_details'] = dict(zip(store_att, store_q[0]))
        dataJson['product_details'] = {'productId':product_q[0][10], 'productName':product_q[0][1], 'productDescription':product_q[0][6], 'material':product_q[0][4], 'brandName':product_q[0][7], 'categoryName':product_q[0][2],'subcategoryName':product_q[0][9], 'productImageUrl':product_q[0][8]}
        return {'status_code':200, 'message': str(len(outputList))+' results found', 'data':dataJson}


def get_variantList_by_id(productId, db):
    product_q = db.query(ProductVariant).filter(ProductVariant.productId==productId).first()
    if product_q==None:
        return {'status_code':200, 'message':'variants do not exist for the product','data':[]}
    else:
        product_q = db.query(ProductVariant.variantId, Colors.color, ProductVariant.colorId, Products.productId, Products.categoryId, Products.subCategoryId, ProductVariant.storeId)\
                      .join(Colors, Colors.colorId==ProductVariant.colorId)\
                      .join(Products, Products.productId==ProductVariant.productId)\
                      .filter(Products.productId==productId).all()
        
        
        spq_att = ['spqId','size', 'sizeId','price', 'quantity']
        outputList = []
        images=[]
        sizes = []
        
        for i in range(len(product_q)):
            size_q = db.query(VariantSizePrice.spqId, Sizes.size, Sizes.sizeId,VariantSizePrice.price, VariantSizePrice.quantity, VariantSizePrice.variantId)\
                        .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                        .filter(VariantSizePrice.variantId==product_q[i][0])\
                        .all()
            image_q = db.query(VariantImages.image_id, VariantImages.image_url)\
                        .filter(VariantImages.variantId==product_q[i][0])\
                        .order_by(VariantImages.variantId)\
                        .all()
            images=[]
            sizes = []
            for size in size_q:
                sizes.append(dict(zip(spq_att, size)))
                
            for image in image_q:
                images.append(image[1])
            
            variant_json = {"variantId":product_q[i][0], 'productId':product_q[i][3],'categoryId':product_q[i][4], 'subCategoryId':product_q[i][5], 'storeId':product_q[i][6],"color":product_q[i][1], 'colorId':product_q[i][2], "spqList":sizes, "imagesUrlList":images}
            outputList.append(variant_json)
        
        return {'status_code':200, 'message': str(len(outputList))+' results found', 'data':outputList}

        

'''
def get_variant(variant_id, db):
    variant_q = db.query(ProductVariant).filter(ProductVariant.variantId==variant_id).first()
    if variant_q==None:
        return {'status_code':0,'message':'variant does not exist', 'data':{}}
    else:
        variant_q = db.query(ProductVariant.variantId, Products.productName,Categories.categoryName, Colors.color, Materials.material, ProductVariant.storeId, Products.productDescription, Brand.brandName, Products.imagesUrl, SubCategories.subcategoryName, Products.productId)\
                        .join(Products, Products.productId==ProductVariant.productId)\
                        .join(Categories, Categories.categoryId==Products.categoryId)\
                        .join(Colors, Colors.colorId==ProductVariant.colorId)\
                        .join(Materials, Materials.materialId==Products.materialId)\
                        .join(Brand, Brand.brandId==Products.brandId)\
                        .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                        .filter(ProductVariant.variantId==variant_id).first()
        
        store_q = db.query(CreateStore.storeId, CreateStore.storeName, CreateStore.locality, CreateStore.district, CreateStore.storePhone, CreateStore.latitude, CreateStore.longitude).filter(CreateStore.storeId==variant_q[5]).first()
            
        store_att= ['storeId','storeName','locality', 'district', 'storePhone','latitude', 'longitude']
        spq_att = ['sqpId', 'size', 'price', 'quantity']
        image_att = ['imageId', 'imageUrl']
        images=[]
        sizes = []
        
        size_q = db.query(VariantSizePrice.spqId, Sizes.size, VariantSizePrice.price, VariantSizePrice.quantity, VariantSizePrice.variantId)\
                    .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                    .filter(VariantSizePrice.variantId==variant_q[0])\
                    .all()
        image_q = db.query(VariantImages.image_id, VariantImages.image_url)\
                    .filter(VariantImages.variantId==variant_q[0])\
                    .order_by(VariantImages.variantId)\
                    .all()
        images=[]
        sizes = []
        for size in size_q:
            sizes.append(dict(zip(spq_att, size)))
            
        for image in image_q:
            images.append(dict(zip(image_att, image)))
        
        variantJson = {"variantId":variant_q[0], 'productId':variant_q[10], "productName":variant_q[1], 'productDescription':variant_q[6], "categoryName":variant_q[2], 'subcategoryName':variant_q[9], "color":variant_q[3], 'brandName':variant_q[7], "material":variant_q[4], "spq":sizes, "images":images}
        variantJson['seller_details'] = dict(zip(store_att, store_q))
        
        
        return {'status_code':200, 'message':'Variant found','data':variantJson}
'''

