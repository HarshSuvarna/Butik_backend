from ast import If
from src.db.models import Countries, CreateStore, Transactions, Users, UserLocations
from datetime import datetime, timedelta
import uuid


def get_user(uid, db, secure):
    user_q = (
        db.query(
            Users.uid,
            Users.mobile,
            Users.cc,
            Users.name,
            Users.dob,
            Users.genderId,
            Users.email,
            Users.isSeller,
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
        )
        .filter(Users.uid == uid, Users.is_deleted == 0)
        .first()
    )

    if user_q != None and secure[0] == user_q.mobile:
        if user_q[7] == 0:
            is_seller = False
        else:
            is_seller = True

        return {
            "status_code": 0,
            "message": "User data",
            "data": {
                "uid": user_q[0],
                "mobile": user_q[1],
                "cc": user_q[2],
                "name": user_q[3],
                "dob": user_q[4],
                "genderId": user_q[5],
                "email": user_q[6],
                "isSeller": is_seller,
                "threeMonthsCredits": user_q[8],
                "sixMonthsCredits": user_q[9],
                "twelveMonthsCredits": user_q[10],
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def add_user(
    uid,
    name,
    mobile,
    cc,
    dob,
    genderId,
    email,
    user_lat,
    user_long,
    country,
    state,
    district,
    locality,
    sub_locality,
    pincode,
    db,
):
    user_info = (
        db.query(Users.is_deleted)
        .filter(Users.mobile == mobile, Users.cc == cc)
        .first()
    )

    if user_info == None:
        new_user = Users(
            uid=uid,
            mobile=mobile,
            cc=cc,
            threeMonthsCredits=0,
            sixMonthsCredits=0,
            twelveMonthsCredits=0,
            name=name,
            dob=dob,
            genderId=genderId,
            email=email,
            isSeller=0,
            is_deleted=0,
            logged_in=1,
            creationTime=datetime.now().replace(microsecond=0),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        u_loc = UserLocations(
            uid=uid,
            user_lat=user_lat,
            user_long=user_long,
            country=country,
            state=state,
            district=district,
            locality=locality,
            sub_locality=sub_locality,
            pincode=pincode,
        )
        db.add(u_loc)
        db.commit()
        user_c = (
            db.query(
                Users.threeMonthsCredits,
                Users.sixMonthsCredits,
                Users.twelveMonthsCredits,
            )
            .filter(Users.uid == uid)
            .first()
        )
        return {
            "status_code": 200,
            "message": "New user created",
            "data": {
                "uid": uid,
                "mobile": mobile,
                "cc": cc,
                "name": name,
                "dob": dob,
                "genderId": genderId,
                "email": email,
                "isSeller": False,
                "threeMonthsCredits": 0,
                "sixMonthsCredits": 0,
                "twelveMonthsCredits": 0,
                "country": country,
                "state": state,
                "district": district,
                "locality": locality,
                "sub_locality": sub_locality,
                "pincode": pincode,
                "user_lat": user_lat,
                "user_long": user_long,
            },
        }

    elif user_info[0] == "1":
        user_q = (
            db.query(Users)
            .filter(Users.mobile == mobile, Users.cc == cc)
            .update({Users.is_deleted: 0})
        )
        db.commit()
        user_iq = db.query(Users).filter(Users.mobile == mobile, Users.cc == cc).first()
        return {"status_code": 200, "message": "Already a user", "data": user_iq}
    else:
        user_q = (
            db.query(Users)
            .filter(Users.cc == cc, Users.mobile == mobile, Users.is_deleted == 0)
            .first()
        )
        return {"status_code": 200, "message": "Already a user", "data": user_q}


def update_user(
    uid,
    name,
    dob,
    gender_id,
    email,
    user_lat,
    user_long,
    country,
    state,
    district,
    locality,
    sub_locality,
    pincode,
    db,
    secure,
):
    user_q = (
        db.query(Users.mobile, Users.cc, Users.isSeller)
        .filter(Users.uid == uid, Users.is_deleted == 0)
        .first()
    )
    print(user_q)
    print(secure[0])

    if user_q != None and secure[0] == user_q.mobile:
        user_info = (
            db.query(Users)
            .filter(Users.uid == uid)
            .update(
                {
                    Users.name: name,
                    Users.dob: dob,
                    Users.genderId: gender_id,
                    Users.email: email,
                    Users.logged_in: 1,
                    Users.last_updated: datetime.now().replace(microsecond=0),
                }
            )
        )
        db.commit()
        ULocation_q = (
            db.query(UserLocations)
            .filter(UserLocations.uid == uid)
            .update(
                {
                    UserLocations.uid: uid,
                    UserLocations.user_long: user_long,
                    UserLocations.user_lat: user_lat,
                    UserLocations.country: country,
                    UserLocations.state: state,
                    UserLocations.district: district,
                    UserLocations.locality: locality,
                    UserLocations.sub_locality: sub_locality,
                    UserLocations.pincode: pincode,
                }
            )
        )
        db.commit()
        if user_q[2] == 0:
            is_seller = False
        else:
            is_seller = True
        return {
            "status_code": 200,
            "message": "User informatin updated successfully",
            "data": {
                "uid": uid,
                "name": name,
                "mobile": user_q[0],
                "cc": user_q[1],
                "dob": dob,
                "genderId": gender_id,
                "email": email,
                "isSeller": is_seller,
                "user_lat": user_lat,
                "user_long": user_long,
                "country": country,
                "state": state,
                "district": district,
                "locality": locality,
                "sub_locality": sub_locality,
                "pincode": pincode,
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to update this resource",
            "data": {},
        }


def delete_user(uid, db, secure):
    user_q = (
        db.query(Users.uid, Users.mobile)
        .filter(Users.uid == uid, Users.is_deleted == 0)
        .first()
    )
    if user_q != None and secure[0] == user_q.mobile:
        user_u = db.query(Users).filter(Users.uid == uid).update({Users.is_deleted: 1})
        db.commit()
        return {
            "status_code": 200,
            "message": "User deleted successfully",
            "data": {"uid": user_q[0]},
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def get_user_bytoken(secure, db):
    user_q = (
        db.query(
            Users.uid,
            Users.mobile,
            Users.cc,
            Users.name,
            Users.dob,
            Users.genderId,
            Users.email,
            Users.isSeller,
            Users.is_deleted,
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
        )
        .filter(Users.mobile == secure[0])
        .first()
    )
    if user_q == None:
        uid = uuid.uuid4()
        new_user = Users(
            uid=uid,
            mobile=secure[0],
            cc=secure[1],
            isSeller=0,
            threeMonthsCredits=0,
            sixMonthsCredits=0,
            twelveMonthsCredits=0,
            is_deleted=0,
            logged_in=1,
            creationTime=datetime.now().replace(microsecond=0),
        )
        db.add(new_user)
        db.commit()
        return {
            "status_code": 200,
            "message": "New user created",
            "data": {
                "uid": uid,
                "mobile": secure[0],
                "cc": secure[1],
                "isSeller": False,
            },
        }

    elif user_q[8] == "1":
        user_q = (
            db.query(Users)
            .filter(Users.mobile == secure[0], Users.cc == secure[1])
            .update({Users.is_deleted: 0})
        )
        db.commit()
        user_iq = (
            db.query(Users)
            .filter(Users.mobile == secure[0], Users.cc == secure[1])
            .first()
        )
        return {"status_code": 200, "message": "New User Created", "data": user_iq}
    else:
        if user_q[7] == 0:
            is_seller = False
        else:
            is_seller = True
        user_loc = (
            db.query(
                UserLocations.user_lat,
                UserLocations.user_long,
                UserLocations.country,
                UserLocations.state,
                UserLocations.district,
                UserLocations.locality,
                UserLocations.sub_locality,
                UserLocations.pincode,
            )
            .filter(UserLocations.uid == user_q[0])
            .first()
        )
        if user_loc == None:
            return {
                "status_code": 200,
                "message": "User data",
                "data": {
                    "uid": user_q[0],
                    "mobile": user_q[1],
                    "cc": user_q[2],
                    "name": user_q[3],
                    "dob": user_q[4],
                    "genderId": user_q[5],
                    "email": user_q[6],
                    "isSeller": is_seller,
                    "threeMonthsCredits": user_q[9],
                    "sixMonthsCredits": user_q[10],
                    "twelveMonthsCredits": user_q[11],
                },
            }
        else:
            return {
                "status_code": 200,
                "message": "User data",
                "data": {
                    "uid": user_q[0],
                    "mobile": user_q[1],
                    "cc": user_q[2],
                    "name": user_q[3],
                    "dob": user_q[4],
                    "genderId": user_q[5],
                    "email": user_q[6],
                    "isSeller": is_seller,
                    "user_lat": user_loc[0],
                    "user_long": user_loc[1],
                    "country": user_loc[2],
                    "state": user_loc[3],
                    "district": user_loc[4],
                    "locality": user_loc[5],
                    "sub_locality": user_loc[6],
                    "pincode": user_loc[7],
                    "threeMonthsCredits": user_q[9],
                    "sixMonthsCredits": user_q[10],
                    "twelveMonthsCredits": user_q[11],
                },
            }


def user_to_seller(uid, db, secure):
    user_q = (
        db.query(
            Users.uid,
            Users.mobile,
            Users.cc,
            Users.name,
            Users.dob,
            Users.email,
            Users.genderId,
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
            Users.isSeller,
        )
        .filter(Users.uid == uid, Users.is_deleted == 0)
        .first()
    )
    
    if user_q != None and secure[0] == user_q.mobile:
        user_u = (
            db.query(Users)
            .filter(Users.uid == uid)
            .update(
                {
                    Users.isSeller: 1,
                    Users.threeMonthsCredits: 15,
                    Users.sixMonthsCredits: 0,
                    Users.twelveMonthsCredits: 0,
                }
            )
        )
        db.commit()
        transactionId = uuid.uuid4()
        transaction_q = Transactions(
            transactionId=transactionId,
            uid=uid,
            credits_3m=15,
            credits_6m=0,
            credits_12m=0,
            totalCredits=15,
            cost_3m=0,
            cost_12m=0,
            cost_6m=0,
            totalCost=0,
            transactionDate=datetime.now().replace(microsecond=0),
            added=1,
            grandTotal=0,
            description="FREE",
        )
        db.add(transaction_q)
        db.commit()
        return {
            "status_code": 200,
            "message": "user converted to seller successfully",
            "data": {
                "uid": user_q[0],
                "mobile": user_q[1],
                "cc": user_q[2],
                "name": user_q[3],
                "dob": user_q[4],
                "email": user_q[5],
                "genderId": user_q[6],
                "threeMonthsCredits": 15,
                "isSeller": True,
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }
