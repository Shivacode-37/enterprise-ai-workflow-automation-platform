from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.asset_request import AssetRequest
from app.models.user import User
from app.schemas.ai_request_api import (
    AIAssetRequestResult,
    AIRequestInput,
    AIRequestResult,
)
from app.services.ai_workflow import build_ai_workflow
from app.models.approval import Approval


router = APIRouter(
    prefix="/ai",
    tags=["AI Request Analysis"],
)


@router.post(
    "/analyze",
    response_model=AIRequestResult,
)
def analyze_asset_request(
    request_data: AIRequestInput,
):
    workflow = build_ai_workflow()

    result = workflow.invoke(
        {
            "user_text": request_data.user_text,
            "analysis": None,
            "error": None,
        }
    )

    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=result["error"],
        )

    return {
        "analysis": result["analysis"],
        "error": None,
    }


@router.post(
    "/requests",
    response_model=AIAssetRequestResult,
    status_code=status.HTTP_201_CREATED,
)

@router.post(
    "/requests",
    response_model=AIAssetRequestResult,
    status_code=status.HTTP_201_CREATED,
)
def create_ai_asset_request(
    request_data: AIRequestInput,
    user_id: int,
    approver_id: int,
    db: Session = Depends(get_db),
):
    # Run the AI workflow
    workflow = build_ai_workflow()
    result = workflow.invoke({
        "user_text": request_data.user_text,
        "analysis": None,
        "error": None,
    })

    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=result["error"],
        )

    analysis = result.get("analysis")
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI analysis did not produce a result.",
        )

    # Validate the employee
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    # Validate the approver
    approver = db.query(User).filter(User.id == approver_id).first()
    if approver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approver not found",
        )

    try:
        # Create the asset request
        asset_request = AssetRequest(
            user_id=user_id,
            request_type=analysis.request_type,
            priority=analysis.priority,
            description=analysis.description,
            status="PENDING",
        )
        db.add(asset_request)
        db.flush()

        # Automatically create its pending approval
        approval = Approval(
            request_id=asset_request.id,
            approver_id=approver_id,
        )
        db.add(approval)

        # Save both records in one transaction
        db.commit()
        db.refresh(asset_request)

    except Exception:
        db.rollback()
        raise

    return {
        "analysis": analysis,
        "asset_request": asset_request,
    }
