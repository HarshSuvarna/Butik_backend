import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.services.attribute_method import (
    get_all_brands,
    get_subcat_by_cat,
    getAllColor,
    getAllCountry,
    getAllMaterial,
    getAllSize,
    getAllcategory,
    getAllgender,
)
from src.authenticate import AuthHandler
from src.db.database import get_db
from src.schemas import (
    BrandNames,
    CategoryIDD,
    CategoryNames,
    ColorNames,
    CountryNames,
    GenderNames,
    GetSizes,
    MaterialNames,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/get-all-brands", tags=["Attributes"])
def get_brands(
    body: BrandNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    return get_all_brands(body.brandNames, db)


@router.post("/getSubcategoryByCategory", tags=["Attributes"])
def get_subcat_by_cats(
    cat: CategoryIDD,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_subcat_by_cat(cat.subCategoryNames, str(cat.categoryId), db)
    return output


@router.post("/getAllCategories", tags=["Attributes"])
def getAllCategories(
    body: CategoryNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllcategory(db, body.categoryNames)
    return output


@router.post("/getAllSizes", tags=["Attributes"])
def getAllSizes(
    size: GetSizes,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllSize(
        size.sizeNames, str(size.categoryId), str(size.subcategoryId), db
    )
    return output


@router.post("/getAllMaterials", tags=["Attributes"])
def getAllMaterials(
    body: MaterialNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllMaterial(body.materialNames, db)
    return output


@router.post("/getAllColors", tags=["Attributes"])
def getAllColors(
    body: ColorNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllColor(body.colorNames, db)
    return output


@router.post("/getAllCountries", tags=["Attributes"])
def getAllCountries(
    body: CountryNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllCountry(body.countryNames, db)
    return output


@router.post("/getAllGenders", tags=["Attributes"])
def getAllGenders(
    body: GenderNames,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getAllgender(body.genderNames, db)
    return output
