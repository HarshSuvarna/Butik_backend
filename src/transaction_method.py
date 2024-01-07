from models import CouponS, Products, Transactions, Users
from datetime import datetime


def post_transaction(
    transactionId,
    uid,
    productId,
    description,
    razorpayPaymentId,
    added,
    credits_3m,
    credits_6m,
    credits_12m,
    totalCredits,
    cost_3m,
    cost_6m,
    cost_12m,
    totalCost,
    discount,
    grandTotal,
    couponId,
    db,
    secure,
):
    if couponId != None:
        coupon_q = db.query(CouponS).filter(CouponS.couponId == str(couponId)).first()
        if not coupon_q:
            return {"status_code": 0, "message": "Coupon ID not valid", "data": {}}
    if added == False:
        product_q = db.query(Products).filter(Products.productId == productId).first()
        if product_q == None:
            return {"status_code": 0, "message": "Product ID not valid", "data": {}}
    user_q = (
        db.query(
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
            Users.mobile,
        )
        .filter(Users.uid == uid)
        .first()
    )
    if user_q != None and user_q.mobile == secure[0]:
        if added == False:
            add = 0
            transaction_q = Transactions(
                transactionId=transactionId,
                uid=uid,
                productId=productId,
                credits_3m=credits_3m,
                credits_6m=credits_6m,
                twelveMonCredit=credits_12m,
                totalCredits=totalCredits,
                transactionDate=datetime.now().replace(microsecond=0),
                description=description,
                razorpayPaymentId=razorpayPaymentId,
                added=add,
                cost_3m=cost_3m,
                cost_6m=cost_6m,
                cost_12m=cost_12m,
                totalCost=totalCost,
                discount=discount,
                grandTotal=grandTotal,
                couponId=couponId,
            )
            db.add(transaction_q)
            db.commit()
            db.refresh(transaction_q)
            trans = (
                db.query(Users)
                .filter(Users.uid == uid)
                .update(
                    {
                        Users.threeMonthsCredits: (int(user_q[0]) - int(credits_3m)),
                        Users.sixMonthsCredits: (int(user_q[1]) - int(credits_6m)),
                        Users.twelveMonthsCredits: (int(user_q[2]) - int(credits_12m)),
                    }
                )
            )
            db.commit()

        else:
            add = 1
            transaction_q = Transactions(
                transactionId=transactionId,
                uid=uid,
                productId=None,
                credits_3m=credits_3m,
                credits_6m=credits_6m,
                credits_12m=credits_12m,
                totalCredits=totalCredits,
                transactionDate=datetime.now().replace(microsecond=0),
                description=description,
                razorpayPaymentId=razorpayPaymentId,
                added=add,
                cost_3m=cost_3m,
                cost_6m=cost_6m,
                cost_12m=cost_12m,
                totalCost=totalCost,
                discount=discount,
                grandTotal=grandTotal,
                couponId=couponId,
            )
            db.add(transaction_q)
            db.commit()
            db.refresh(transaction_q)

            trans = (
                db.query(Users)
                .filter(Users.uid == uid)
                .update(
                    {
                        Users.threeMonthsCredits: (int(user_q[0]) + int(credits_3m)),
                        Users.sixMonthsCredits: (int(user_q[1]) + int(credits_6m)),
                        Users.twelveMonthsCredits: (int(user_q[2]) + int(credits_12m)),
                    }
                )
            )
            db.commit()

        transac = (
            db.query(Transactions.transactionDate)
            .filter(Transactions.transactionId == transactionId)
            .first()
        )
        if added == False:
            return {
                "status_code": 200,
                "message": "Transaction added successfully",
                "data": {
                    "transactionId": transactionId,
                    "uuid": uid,
                    "productId": productId,
                    "credits_3m": credits_3m,
                    "credits_6m": credits_6m,
                    "credits_12m": credits_12m,
                    "totalCredits": totalCredits,
                    "cost_3m": cost_3m,
                    "cost_6m": cost_6m,
                    "cost_12m": cost_12m,
                    "totalCost": totalCost,
                    "discount": discount,
                    "grandTotal": grandTotal,
                    "description": description,
                    "couponId": couponId,
                    "razorpayPaymentId": razorpayPaymentId,
                    "added": added,
                    "transactionDate": transac[0],
                },
            }
        else:
            return {
                "status_code": 200,
                "message": "Transaction added successfully",
                "data": {
                    "transactionId": transactionId,
                    "uuid": uid,
                    "productId": None,
                    "credits_3m": credits_3m,
                    "credits_6m": credits_6m,
                    "credits_12m": credits_12m,
                    "totalCredits": totalCredits,
                    "cost_3m": cost_3m,
                    "cost_6m": cost_6m,
                    "cost_12m": cost_12m,
                    "totalCost": totalCost,
                    "discount": discount,
                    "grandTotal": grandTotal,
                    "description": description,
                    "couponId": couponId,
                    "razorpayPaymentId": razorpayPaymentId,
                    "added": added,
                    "transactionDate": transac[0],
                },
            }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }


def get_transaction(uid, db, secure):
    user_q = (
        db.query(
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
            Users.mobile,
        )
        .filter(Users.uid == uid)
        .first()
    )
    if user_q != None and user_q.mobile == secure[0]:
        trans_q = (
            db.query(
                Transactions.transactionId,
                Transactions.uid,
                Transactions.productId,
                Transactions.description,
                Transactions.razorpayPaymentId,
                Transactions.added,
                Transactions.credits_3m,
                Transactions.credits_6m,
                Transactions.credits_12m,
                Transactions.totalCredits,
                Transactions.cost_3m,
                Transactions.cost_6m,
                Transactions.cost_12m,
                Transactions.totalCost,
                Transactions.discount,
                Transactions.grandTotal,
                Transactions.couponId,
                Transactions.transactionDate,
            )
            .filter(Transactions.uid == uid)
            .order_by(Transactions.transactionDate.desc())
            .all()
        )

        outputList = []
        trans_att = [
            "transactionId",
            "uid",
            "productIds",
            "description",
            "razorpayPaymentId",
            "added",
            "credits_3m",
            "credits_6m",
            "credits_12m",
            "totalCredits",
            "cost_3m",
            "cost_6m",
            "cost_12m",
            "totalCost",
            "discount",
            "grandTotal",
            "couponId",
            "transactionDate",
        ]

        for transaction in trans_q:
            transDict = dict(zip(trans_att, transaction))
            if transDict["added"] == 0:
                transDict["added"] = False
            else:
                transDict["added"] = True
            outputList.append(transDict)
        return {
            "status_code": 200,
            "message": str(len(outputList)) + " results found",
            "data": outputList,
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": [],
        }


def get_couponCode(db):
    coupon_q = db.query(CouponS.couponId, CouponS.couponCode).all()
    if coupon_q == None:
        return {"status_code": 0, "data": []}
    else:
        outputList = []
        coupon_att = ["couponId", "couponCode"]
        for coupon in coupon_q:
            outputList.append(dict(zip(coupon_att, coupon)))
        return {"status_code": 0, "data": outputList}


def getCreditBalance(uid, db, secure):
    print(uid)
    user_q = (
        db.query(
            Users.threeMonthsCredits,
            Users.sixMonthsCredits,
            Users.twelveMonthsCredits,
            Users.mobile,
        )
        .filter(Users.uid == uid)
        .first()
    )
    if user_q != None and user_q[3] == secure[0]:
        return {
            "status_code": 200,
            "message": "Credits found",
            "data": {
                "threeMonthsCredits": user_q[0],
                "sixMonthsCredits": user_q[1],
                "twelveMonthsCredits": user_q[2],
                "mobile": user_q[3],
            },
        }
    else:
        return {
            "status_code": 0,
            "message": "You are not Authorized to access this resource",
            "data": {},
        }
