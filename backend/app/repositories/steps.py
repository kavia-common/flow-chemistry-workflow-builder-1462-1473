from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.step import Step

# PUBLIC_INTERFACE
def list_steps_for_experiment(db: Session, experiment_id: int) -> List[Step]:
    """List steps for an experiment ordered by order_index."""
    stmt = select(Step).where(Step.experiment_id == experiment_id).order_by(Step.order_index.asc(), Step.id.asc())
    return list(db.execute(stmt).scalars().all())

# PUBLIC_INTERFACE
def create_step(db: Session, experiment_id: int, name: str, type: str | None, order_index: int, notes: str | None) -> Step:
    """Create a new step for an experiment."""
    step = Step(experiment_id=experiment_id, name=name, type=type, order_index=order_index, notes=notes)
    db.add(step)
    db.commit()
    db.refresh(step)
    return step

# PUBLIC_INTERFACE
def update_step(db: Session, step_id: int, name: str | None, type: str | None, order_index: int | None, notes: str | None) -> Optional[Step]:
    """Update a step."""
    step = db.get(Step, step_id)
    if not step:
        return None
    if name is not None:
        step.name = name
    if type is not None:
        step.type = type
    if order_index is not None:
        step.order_index = order_index
    if notes is not None:
        step.notes = notes
    db.add(step)
    db.commit()
    db.refresh(step)
    return step

# PUBLIC_INTERFACE
def delete_step(db: Session, step_id: int) -> bool:
    """Delete a step by id."""
    step = db.get(Step, step_id)
    if not step:
        return False
    db.delete(step)
    db.commit()
    return True
