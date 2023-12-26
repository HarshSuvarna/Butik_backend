from models import (
    Categories,
    Brand,
    Colors,
    Countries,
    Genders,
    Materials,
    Sizes,
    SubCategories,
)


def get_all_brands(brandNames, db):
    if brandNames and len(brandNames):
        brandNameObject = {}
        brandNames = db.query(Brand).filter(Brand.brandName.in_(brandNames)).all()
        for brand in brandNames:
            brandNameObject[brand.brandName] = brand
        return brandNameObject
    brand_q = db.query(Brand.brandId, Brand.brandName).order_by(Brand.brandId).all()
    brand_att = ["brandId", "brandName"]
    outputList = []
    for brand in brand_q:
        outputList.append(dict(zip(brand_att, brand)))
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def get_subcat_by_cat(subCatNames, categoryId, db):
    if subCatNames and len(subCatNames):
        subCatNamesObject = {}
        subcatNames = (
            db.query(SubCategories)
            .filter(SubCategories.subcategoryName.in_(subCatNames))
            .all()
        )
        for subcat in subcatNames:
            subCatNamesObject[subcat.subcategoryName] = subcat
        return subCatNamesObject

    cat_q = db.query(Categories).filter(Categories.categoryId == categoryId).first()
    if cat_q == None:
        return {"status_code": 0, "message": "category does not exist", "data": []}
    else:
        subcat_q = (
            db.query(
                SubCategories.subcategoryId,
                SubCategories.subcategoryName,
                SubCategories.categoryId,
            )
            .filter(SubCategories.categoryId == categoryId)
            .order_by(SubCategories.subcategoryId)
            .all()
        )
        subcat_att = ["subcategoryId", "subcategoryName", "categoryId"]
        outputList = []
        for subcat in subcat_q:
            outputList.append(dict(zip(subcat_att, subcat)))
        return {
            "status_code": 0,
            "message": str(len(outputList)) + " results found",
            "data": outputList,
        }


def getAllcategory(db, catNames):
    if catNames and len(catNames):
        catNameObject = {}
        catNames = (
            db.query(Categories).filter(Categories.categoryName.in_(catNames)).all()
        )
        for cat in catNames:
            catNameObject[cat.categoryName] = cat
        return catNameObject

    category_q = db.query(Categories).order_by(Categories.categoryId).all()
    outputList = []
    for cat in category_q:
        outputList.append(cat)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def getAllSize(sizeNames, categoryId, subcategoryId, db):
    if sizeNames and len(sizeNames):
        sizeNameObject = {}
        sizeName = db.query(Sizes).filter(Sizes.size.in_(sizeNames)).all()
        for size in sizeName:
            sizeNameObject[size.size] = size
        return sizeNameObject
    size_q = (
        db.query(Sizes)
        .filter(Sizes.categoryId == categoryId, Sizes.subcategoryId == subcategoryId)
        .order_by(Sizes.sizeId)
        .all()
    )
    outputList = []
    for size in size_q:
        outputList.append(size)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def getAllMaterial(materialNames, db):
    if materialNames and len(materialNames):
        materialNameObject = {}
        materialName = (
            db.query(Materials).filter(Materials.material.in_(materialNames)).all()
        )
        for material in materialName:
            materialNameObject[material.material] = material
        return materialNameObject
    mat_q = db.query(Materials).order_by(Materials.materialId).all()
    outputList = []
    for mat in mat_q:
        outputList.append(mat)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def getAllColor(colorNames, db):
    if colorNames and len(colorNames):
        colorNameObject = {}
        colorName = db.query(Colors).filter(Colors.color.in_(colorNames)).all()
        for color in colorName:
            colorNameObject[color.color] = color
        return colorNameObject
    color_q = db.query(Colors).order_by(Colors.colorId).all()
    outputList = []
    for color in color_q:
        outputList.append(color)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def getAllCountry(countryNames, db):
    if countryNames and len(countryNames):
        countryNameObject = {}
        countryName = (
            db.query(Countries).filter(Countries.country.in_(countryNames)).all()
        )
        for country in countryName:
            countryNameObject[country.country] = country
        return countryNameObject
    country_q = db.query(Countries).order_by(Countries.countryId).all()
    outputList = []
    for country in country_q:
        outputList.append(country)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }


def getAllgender(genderNames, db):
    if genderNames and len(genderNames):
        genderNameObject = {}
        genderName = db.query(Genders).filter(Genders.gender.in_(genderNames)).all()
        for gender in genderName:
            genderNameObject[gender.gender] = gender
        return genderNameObject
    gender_q = db.query(Genders).order_by(Genders.genderId).all()
    outputList = []
    for gender in gender_q:
        outputList.append(gender)
    return {
        "status_code": 0,
        "message": str(len(outputList)) + " results found",
        "data": outputList,
    }
