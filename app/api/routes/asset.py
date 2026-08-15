from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.assets import Asset
from app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate


router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


# POST /assets/
@router.post(
    "/",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
):
    asset = Asset(
        asset_type=asset_data.asset_type,
        name=asset_data.name,
        serial_number=asset_data.serial_number,
        location=asset_data.location,
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


# GET /assets/
@router.get(
    "/",
    response_model=list[AssetResponse],
)
def get_assets(
    db: Session = Depends(get_db),
):
    assets = db.query(Asset).all()

    return assets


# GET /assets/{asset_id}
@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return asset


# PATCH /assets/{asset_id}
@router.patch(
    "/{asset_id}",
    response_model=AssetResponse,
)
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    update_data = asset_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return asset


# DELETE /assets/{asset_id}
@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    db.delete(asset)
    db.commit()
