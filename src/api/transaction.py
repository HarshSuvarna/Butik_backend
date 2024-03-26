import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session

from src.authenticate import AuthHandler
from src.db.database import get_db
from src.schemas import TransactionC, UserID
from src.services.transaction_method import (
    get_couponCode,
    get_transaction,
    getCreditBalance,
    post_transaction,
)

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/get_transactions_by_userId", tags=["Transactions"])
def get_transacitons(
    transaction: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = get_transaction(str(transaction.uid), db, secure)
    return output


@router.post("/create_transaction", tags=["Transactions"])
def post_transactions(
    transaction: TransactionC,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    transactionId = uuid.uuid4()
    output = post_transaction(
        str(transactionId),
        str(transaction.uid),
        str(transaction.productId),
        transaction.description,
        transaction.razorpayPaymentId,
        transaction.added,
        transaction.credits_3m,
        transaction.credits_6m,
        transaction.credits_12m,
        transaction.totalCredits,
        transaction.cost_3m,
        transaction.cost_6m,
        transaction.cost_12m,
        transaction.totalCost,
        transaction.discount,
        transaction.grandTotal,
        transaction.couponId,
        db,
        secure,
    )
    return output


@router.get("/get_couponCodes", tags=["Transactions"])
def get_couponCodes(
    db: Session = Depends(get_db), secure=Depends(auth_handler.auth_wrapper)
):
    output = get_couponCode(db)
    return output


@router.post("/getCreditBalance", tags=["Transactions"])
def getCreditBalances(
    user: UserID,
    db: Session = Depends(get_db),
    secure=Depends(auth_handler.auth_wrapper),
):
    output = getCreditBalance(str(user.uid), db, secure)
    return output
