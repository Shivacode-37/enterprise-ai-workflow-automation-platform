from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.asset_request import AssetRequest
from app.models.user import User
from app.schemas.asset_request import (
    AssetRequestCreate,
    AssetRequestResponse,
    AssetRequestUpdate
)


router = APIRouter(
    prefix="/asset-requests",
    tags=["Asset Requests"],
)


# POST /asset-requests/
@router.post(
    "/",
    response_model=AssetRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset_request(
    request_data: AssetRequestCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == request_data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    asset_request = AssetRequest(
        user_id=request_data.user_id,
        request_type=request_data.request_type,
        priority=request_data.priority,
        description=request_data.description,
    )

    db.add(asset_request)
    db.commit()
    db.refresh(asset_request)

    return asset_request


# GET /asset-requests/
@router.get(
    "/",
    response_model=list[AssetRequestResponse],
)
def get_asset_requests(
    db: Session = Depends(get_db),
):
    asset_requests = db.query(AssetRequest).all()

    return asset_requests


# GET /asset-requests/{request_id}
@router.get(
    "/{request_id}",
    response_model=AssetRequestResponse,
)
def get_asset_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    asset_request = (
        db.query(AssetRequest)
        .filter(AssetRequest.id == request_id)
        .first()
    )

    if asset_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset request not found",
        )

    return asset_request

# PATCH /asset-requests/{request_id}
@router.patch(
    "/{request_id}",
    response_model=AssetRequestResponse,
)
def update_asset_request(
    request_id: int,
    request_data: AssetRequestUpdate,
    db: Session = Depends(get_db),
):
    asset_request = (
        db.query(AssetRequest)
        .filter(AssetRequest.id == request_id)
        .first()
    )

    if asset_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset request not found",
        )

    update_data = request_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset_request, field, value)

    db.commit()
    db.refresh(asset_request)

    return asset_request


@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_asset_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    asset_request = (
        db.query(AssetRequest)
        .filter(AssetRequest.id == request_id)
        .first()
    )

    if asset_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset request not found",
        )

    db.delete(asset_request)
    db.commit()
