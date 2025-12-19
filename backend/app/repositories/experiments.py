from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.experiment import Experiment
from ..models.step import Step

# PUBLIC_INTERFACE
def list_experiments(db: Session) -> List[Experiment]:
    """Return all experiments ordered by created_at desc."""
    stmt = select(Experiment).order_by(Experiment.created_at.desc())
    return list(db.execute(stmt).scalars().all())

# PUBLIC_INTERFACE
def get_experiment(db: Session, experiment_id: int) -> Optional[Experiment]:
    """Return a single experiment by id."""
    return db.get(Experiment, experiment_id)

# PUBLIC_INTERFACE
def get_experiment_with_steps(db: Session, experiment_id: int) -> Optional[Tuple[Experiment, List[Step]]]:
    """Return experiment and its steps ordered by order_index."""
    exp = db.get(Experiment, experiment_id)
    if exp is None:
        return None
    # Eagerly load sorted steps
    steps_sorted = sorted(exp.steps, key=lambda s: (s.order_index, s.id))
    return exp, steps_sorted

# PUBLIC_INTERFACE
def create_experiment(db: Session, name: str, description: Optional[str], status: str = "draft") -> Experiment:
    """Create a new experiment."""
    exp = Experiment(name=name, description=description, status=status)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

# PUBLIC_INTERFACE
def update_experiment(db: Session, experiment_id: int, name: Optional[str], description: Optional[str], status: Optional[str]) -> Optional[Experiment]:
    """Update fields on an experiment."""
    exp = db.get(Experiment, experiment_id)
    if not exp:
        return None
    if name is not None:
        exp.name = name
    if description is not None:
        exp.description = description
    if status is not None:
        exp.status = status
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

# PUBLIC_INTERFACE
def delete_experiment(db: Session, experiment_id: int) -> bool:
    """Delete experiment by id."""
    exp = db.get(Experiment, experiment_id)
    if not exp:
        return False
    db.delete(exp)
    db.commit()
    return True
