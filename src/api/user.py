import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.authenticate import AuthHandler
from src.db.database import get_db
from src.schemas import UpdateUser, UserCreate, UserID

from src.services.user_method import (
    add_user,
    delete_user,
    get_user,
    get_user_bytoken,
    update_user,
    user_to_seller,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/create_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
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


@router.post("/get_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
def get_users(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_user(str(user.uid), db, secure)
    return output


@router.get("/getUserByToken", tags=["User"])
def get_user_bytokens(
    db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = get_user_bytoken(secure, db)
    return output


@router.put("/update_user", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
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


@router.delete("/delete_user", tags=["User"])
def delete_users(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = delete_user(str(user.uid), db, secure)
    return output


@router.post("/userToSeller", tags=["User"])
def user_to_sellers(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = user_to_seller(str(user.uid), db, secure)
    return output
