from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.approval import Approval
from app.models.asset_request import AssetRequest
from app.models.user import User
from app.schemas.approval import (
    ApprovalCreate,
    ApprovalDecision,
    ApprovalResponse,
)
from app.models.workflow_run import WorkflowRun
from uuid import uuid4

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


@router.post(
    "/",
    response_model=ApprovalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_approval(
    approval_data: ApprovalCreate,
    db: Session = Depends(get_db),
):
    # Check whether Asset Request exists
    asset_request = (
        db.query(AssetRequest)
        .filter(AssetRequest.id == approval_data.request_id)
        .first()
    )

    if asset_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset request not found",
        )

    # Check whether Approver exists
    approver = (
        db.query(User)
        .filter(User.id == approval_data.approver_id)
        .first()
    )

    if approver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approver not found",
        )

    approval = Approval(
        request_id=approval_data.request_id,
        approver_id=approval_data.approver_id,
    )

    existing_approval = (
    db.query(Approval)
    .filter(
        Approval.request_id == approval_data.request_id,
        Approval.approver_id == approval_data.approver_id,
    )
    .first()
)

    if existing_approval is not None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Approval already exists for this request and approver",
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval

@router.get(
    "/",
    response_model=list[ApprovalResponse],
)
def get_approvals(
    db: Session = Depends(get_db),
):
    approvals = (
        db.query(Approval)
        .order_by(Approval.created_at.desc())
        .all()
    )

    return approvals


@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
def get_approval(
    approval_id: int,
    db: Session = Depends(get_db),
):
    approval = (
        db.query(Approval)
        .filter(Approval.id == approval_id)
        .first()
    )

    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    return approval



@router.patch(
    "/{approval_id}/decision",
    response_model=ApprovalResponse,
)

def decide_approval(
    approval_id: int,
    decision_data: ApprovalDecision,
    db: Session = Depends(get_db),
):
    approval = (
        db.query(Approval)
        .filter(Approval.id == approval_id)
        .first()
    )

    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    if approval.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approval has already been decided",
        )

    if decision_data.status == "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision must be APPROVED or REJECTED",
        )

    asset_request = (
        db.query(AssetRequest)
        .filter(AssetRequest.id == approval.request_id)
        .first()
    )

    if asset_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related asset request not found",
        )

    approval.status = decision_data.status.value
    approval.comments = decision_data.comments
    approval.decided_at = datetime.now(timezone.utc)

    asset_request.status = decision_data.status.value
    if decision_data.status.value == "APPROVED":
        workflow_run = WorkflowRun(
        request_id=asset_request.id,
        workflow_id=str(uuid4()),
        status="RUNNING",
        current_step="WORKFLOW_STARTED",
    )
        db.add(workflow_run)

    

    db.commit()
    db.refresh(approval)

    return approval


