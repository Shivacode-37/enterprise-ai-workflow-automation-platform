from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    request_id: int | None,
    actor_type: str,
    action: str,
    details: str | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        request_id=request_id,
        actor_type=actor_type,
        action=action,
        details=details,
    )

    db.add(audit_log)

    return audit_log
