from models import Brand, Categories, Colors, CreateStore, Genders, Materials, ProductVariant, Products, Sizes, SubCategories, VariantSizePrice, VariantImages


def product_filter(storeIds, brandIds,colorIds, sizeIds, materialIds, categoryIds, subcategoryIds, genderIds, maxPrices,db):
     
    if (len(sizeIds)!=0) or (len(maxPrices)!=0):
        product_q = db.query(Products.productId, ProductVariant.variantId,Colors.color, Brand.brandName, Materials.material, 
                             Categories.categoryName, SubCategories.subcategoryName, Genders.gender, CreateStore.storeName, 
                             Products.productName, Products.productDescription)\
                        .join(CreateStore, CreateStore.storeId==Products.storeId)\
                        .join(ProductVariant, ProductVariant.productId==Products.productId)\
                        .join(Brand, Brand.brandId==Products.brandId)\
                        .join(Colors, Colors.colorId==ProductVariant.colorId)\
                        .join(Materials, Materials.materialId==Products.materialId)\
                        .join(Categories, Categories.categoryId==Products.categoryId)\
                        .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                        .join(Genders, Genders.genderId==Products.genderId)\
                        .join(VariantSizePrice, VariantSizePrice.variantId==ProductVariant.variantId)\
                        .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                        
    else:
        product_q = db.query(Products.productId, ProductVariant.variantId,Colors.color, Brand.brandName, Materials.material, 
                             Categories.categoryName, SubCategories.subcategoryName, Genders.gender, CreateStore.storeName,
                             Products.productName, Products.productDescription)\
                        .join(CreateStore, CreateStore.storeId==Products.storeId)\
                        .join(ProductVariant, ProductVariant.productId==Products.productId)\
                        .join(Brand, Brand.brandId==Products.brandId)\
                        .join(Colors, Colors.colorId==ProductVariant.colorId)\
                        .join(Materials, Materials.materialId==Products.materialId)\
                        .join(Categories, Categories.categoryId==Products.categoryId)\
                        .join(SubCategories, SubCategories.subcategoryId==Products.subCategoryId)\
                        .join(Genders, Genders.genderId==Products.genderId)
                        

    counter=0   
    if len(storeIds)!=0:
        product_q = product_q.filter(Products.storeId.in_(storeIds), Products.is_deleted==0)
        counter+=1
    if len(brandIds)!=0:
        product_q = product_q.filter(Products.brandId.in_(brandIds), Products.is_deleted==0)
        counter+=1
    if len(colorIds)!=0:
        product_q = product_q.filter(ProductVariant.colorId.in_(colorIds))
        counter+=1
    if len(materialIds)!=0:
        product_q = product_q.filter(Products.materialId.in_(materialIds))
        counter+=1
    if len(categoryIds)!=0:
        product_q = product_q.filter(Products.categoryId.in_(categoryIds))
        counter+=1
    if len(subcategoryIds)!=0:
        product_q = product_q.filter(Products.subCategoryId.in_(subcategoryIds))
        counter+=1
    if len(genderIds)!=0:
        product_q = product_q.filter(Products.genderId.in_(genderIds))
        counter+=1
    if len(maxPrices)!=0:
        product_q = product_q.filter(VariantSizePrice.price.between(maxPrices[0],maxPrices[1]))
        counter+=1
    if len(sizeIds)!=0:
        product_q = product_q.filter(VariantSizePrice.sizeId.in_(sizeIds))
        counter+=1
    
    
    final = product_q.filter(Products.is_deleted==0, ProductVariant.is_deleted==0).all()
    spq_att = ['size', 'price', 'quantity']
    outputList=[]
    newOpList = []
    if (len(sizeIds)!=0):
        for i in range(len(final)):
            size_q = db.query(Sizes.size, VariantSizePrice.price, VariantSizePrice.quantity, VariantSizePrice.variantId)\
                        .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                        .filter(VariantSizePrice.variantId==final[i][1], VariantSizePrice.sizeId.in_(sizeIds))\
                        .all()
            
            image_q = db.query(VariantImages.image_url)\
                        .filter(VariantImages.variantId==product_q[i][1])\
                        .order_by(VariantImages.variantId)\
                        .all()
            images=[]
            sizes = []
            for size in size_q:
                sizes.append(dict(zip(spq_att, size)))
                
            for image in image_q:
                images.append(image[0])
            
            variant_json = {"productId":final[i][0], "variantId": final[i][1], "color": final[i][2], "brandName": final[i][3],\
                            "material": final[i][4],"categoryName": final[i][5], "subcategoryName": final[i][6], "gender": final[i][7], 
                            "storeName":final[i][8], "productName":final[i][9], "productDescription":final[i][10], "spq":sizes,"images":images}
            outputList.append(variant_json)
            newOpList = []
            newSpq = []
            for i in range(len(outputList)):
                if i==len(outputList)-1:
                #     if len(maxPrices)!=0:
                #         for spq in outputList[i]["spq"]:
                #             if maxPrices[0] <= spq["price"] <=maxPrices[1]:
                #                 newSpq.append(spq)
                #         outputList[i]["spq"] = newSpq
                    newOpList.append(outputList[i])
                    break
                if outputList[i+1]['variantId']!=outputList[i]['variantId']:
                    # if len(maxPrices)!=0:
                    #     for spq in outputList[i]["spq"]:
                    #         if maxPrices[0] <= spq["price"] <=maxPrices[1]:
                    #             newSpq.append(spq)
                    #     outputList[i]["spq"] = newSpq
                    newOpList.append(outputList[i])
            if len(maxPrices)!=0:
                for i in range(len(newOpList)):
                    newSpq=[]
                    for spq in newOpList[i]["spq"]:
                        if int(maxPrices[0]) <= int(spq["price"]) <=int(maxPrices[1]):
                            newSpq.append(spq)
                    newOpList[i]["spq"] = newSpq  

    else:
        for i in range(len(final)):
                size_q = db.query(Sizes.size, VariantSizePrice.price, VariantSizePrice.quantity, VariantSizePrice.variantId)\
                            .join(Sizes, Sizes.sizeId==VariantSizePrice.sizeId)\
                            .filter(VariantSizePrice.variantId==final[i][1])\
                            .all()

                image_q = db.query(VariantImages.image_url)\
                            .filter(VariantImages.variantId==product_q[i][1])\
                            .order_by(VariantImages.variantId)\
                            .all()
                images=[]
                sizes = []
                for size in size_q:
                    sizes.append(dict(zip(spq_att, size)))
                    
                for image in image_q:
                    images.append(image[0])
                
                variant_json = {"productId":final[i][0], "variantId": final[i][1], "color": final[i][2], "brandName": final[i][3],\
                                "material": final[i][4],"categoryName": final[i][5], "subcategoryName": final[i][6], "gender": final[i][7], 
                                "storeName":final[i][8], "productName":final[i][9], "productDescription":final[i][10],"spq":sizes,"images":images}
                outputList.append(variant_json)
        
        for i in range(len(outputList)):
            if i==len(outputList)-1:
                newOpList.append(outputList[i])
                break
            if outputList[i+1]['variantId']!=outputList[i]['variantId']:
                newOpList.append(outputList[i])
        if len(maxPrices)!=0:
            for i in range(len(newOpList)):
                newSpq=[]
                for spq in newOpList[i]["spq"]:
                    if int(maxPrices[0]) <= int(spq["price"]) <=int(maxPrices[1]):
                        newSpq.append(spq)
                newOpList[i]["spq"] = newSpq   
                

    return {'status_code':200,'Filters Applied':counter, 'message': str(len(newOpList))+' results found', 'data':newOpList}



