from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.connection import get_db
from app.models.workflow_run import WorkflowRun
from app.schemas.workflow_run import WorkflowRunResponse, WorkflowRunUpdate


router = APIRouter(
    prefix="/workflow-runs",
    tags=["Workflow Runs"],
)


@router.get(
    "/",
    response_model=list[WorkflowRunResponse],
)
def get_workflow_runs(
    db: Session = Depends(get_db),
):
    workflow_runs = (
        db.query(WorkflowRun)
        .order_by(WorkflowRun.started_at.desc())
        .all()
    )

    return workflow_runs


@router.get(
    "/{workflow_id}",
    response_model=WorkflowRunResponse,
)
def get_workflow_run(
    workflow_id: str,
    db: Session = Depends(get_db),
):
    workflow_run = (
        db.query(WorkflowRun)
        .filter(WorkflowRun.workflow_id == workflow_id)
        .first()
    )

    if workflow_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found",
        )

    return workflow_run


@router.patch(
    "/{workflow_id}",
    response_model=WorkflowRunResponse,
)
def update_workflow_run(
    workflow_id: str,
    workflow_data: WorkflowRunUpdate,
    db: Session = Depends(get_db),
):
    workflow_run = (
        db.query(WorkflowRun)
        .filter(WorkflowRun.workflow_id == workflow_id)
        .first()
    )

    if workflow_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found",
        )

    allowed_transitions = {
    "RUNNING": {"PROCESSING", "FAILED"},
    "PROCESSING": {"COMPLETED", "FAILED"},
    "COMPLETED": set(),
    "FAILED": set(),
}

    if workflow_data.status not in allowed_transitions.get(
    workflow_run.status,
    set(),
):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            f"Invalid workflow status transition: "
            f"{workflow_run.status} → {workflow_data.status}"
        ),
    )

    workflow_run.status = workflow_data.status

    if workflow_data.current_step is not None:
        workflow_run.current_step = workflow_data.current_step

    if workflow_data.status in {"COMPLETED", "FAILED"}:
        workflow_run.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(workflow_run)

    return workflow_run
