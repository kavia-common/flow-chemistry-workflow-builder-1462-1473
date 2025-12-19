from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..schemas import StepSchema, CreateStepRequest, UpdateStepRequest
from ..db import get_session
from ..repositories import steps as repo
from ..repositories import experiments as exp_repo

blp = Blueprint(
    "Steps",
    "steps",
    url_prefix="/steps",
    description="CRUD operations for Steps",
)

@blp.route("/experiment/<int:experiment_id>")
class StepsByExperiment(MethodView):
    """List and create steps for a given experiment."""

    @blp.response(200, StepSchema(many=True), description="List steps by experiment")
    def get(self, experiment_id: int):
        """List steps for experiment."""
        db = get_session()
        try:
            # Ensure experiment exists
            if exp_repo.get_experiment(db, experiment_id) is None:
                abort(404, description="Experiment not found")
            return repo.list_steps_for_experiment(db, experiment_id)
        finally:
            db.close()

    @blp.arguments(CreateStepRequest, location="json")
    @blp.response(201, StepSchema, description="Created step")
    def post(self, payload, experiment_id: int):
        """Create a step under the experiment."""
        db = get_session()
        try:
            if exp_repo.get_experiment(db, experiment_id) is None:
                abort(404, description="Experiment not found")
            step = repo.create_step(
                db,
                experiment_id=experiment_id,
                name=payload.get("name"),
                type=payload.get("type"),
                order_index=payload.get("order_index", 0),
                notes=payload.get("notes"),
            )
            return step
        finally:
            db.close()

@blp.route("/<int:step_id>")
class StepDetail(MethodView):
    """Update and delete a step."""

    @blp.arguments(UpdateStepRequest, location="json")
    @blp.response(200, StepSchema, description="Updated step")
    def patch(self, payload, step_id: int):
        """Update a step by ID."""
        db = get_session()
        try:
            step = repo.update_step(
                db,
                step_id=step_id,
                name=payload.get("name"),
                type=payload.get("type"),
                order_index=payload.get("order_index"),
                notes=payload.get("notes"),
            )
            if step is None:
                abort(404, description="Step not found")
            return step
        finally:
            db.close()

    @blp.response(204, description="Deleted")
    def delete(self, step_id: int):
        """Delete a step by ID."""
        db = get_session()
        try:
            ok = repo.delete_step(db, step_id)
            if not ok:
                abort(404, description="Step not found")
            return ""
        finally:
            db.close()
