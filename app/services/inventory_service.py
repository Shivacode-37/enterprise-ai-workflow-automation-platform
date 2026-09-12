from sqlalchemy.orm import Session
from app.models.asset_request import AssetRequest
from app.models.assets import Asset


def find_available_asset(
    db: Session,
    asset_type: str,
) -> Asset | None:
    return (
        db.query(Asset)
        .filter(
            Asset.asset_type == asset_type.upper(),
            Asset.status == "AVAILABLE",
            Asset.assigned_to.is_(None),
        )
        .first()
    )
# The query will look for,So it won't accidently allocate laptop which is already assigned.
# asset_type = LAPTOP
#        AND
# status = AVAILABLE
#        AND
# assigned_to IS NULL
def assign_asset(
    db: Session,
    asset: Asset,
    user_id: int,
) -> Asset:
    asset.status = "ASSIGNED"
    asset.assigned_to = user_id
    return asset

def allocate_asset_for_request(
    db: Session,
    request: AssetRequest,
) -> Asset | None:
    asset = find_available_asset(
        db,
        request.request_type,
    )

    if asset is None:
        return None

    return assign_asset(
        db,
        asset,
        request.user_id,
    )
