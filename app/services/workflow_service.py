from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.workflow_run import WorkflowRun
from app.services.inventory_service import allocate_asset_for_request
from app.services.audit_service import create_audit_log


def execute_workflow(
    db: Session,
    workflow_run: WorkflowRun,
):
    request = workflow_run.request

    workflow_run.status = "PROCESSING"
    workflow_run.current_step = "INVENTORY_ALLOCATION"

    asset = allocate_asset_for_request(
        db,
        request,
    )

    if asset is None:
        workflow_run.status = "FAILED"
        workflow_run.current_step = "INVENTORY_UNAVAILABLE"
        workflow_run.completed_at = datetime.now(timezone.utc)

        create_audit_log(
            db=db,
            request_id=request.id,
            actor_type="WORKFLOW",
            action="INVENTORY_ALLOCATION_FAILED",
            details=f"No available asset found for type {request.request_type}",
        )

        db.commit()
        db.refresh(workflow_run)

        return workflow_run

    create_audit_log(
        db=db,
        request_id=request.id,
        actor_type="WORKFLOW",
        action="ASSET_ASSIGNED",
        details=f"Asset {asset.serial_number} assigned to user {request.user_id}",
    )

    workflow_run.status = "COMPLETED"
    workflow_run.current_step = "ASSET_ASSIGNED"
    workflow_run.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(workflow_run)

    return workflow_run
