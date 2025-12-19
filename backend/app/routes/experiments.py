from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..schemas import (
    ExperimentSchema,
    ExperimentWithStepsSchema,
    CreateExperimentRequest,
    UpdateExperimentRequest,
)
from ..db import get_session
from ..repositories import experiments as repo


blp = Blueprint(
    "Experiments",
    "experiments",
    url_prefix="/experiments",
    description="CRUD operations for Experiments",
)

@blp.route("/")
class ExperimentsList(MethodView):
    """List and create experiments."""

    @blp.response(200, ExperimentSchema(many=True), description="List experiments")
    def get(self):
        """List all experiments ordered by created date."""
        db = get_session()
        try:
            items = repo.list_experiments(db)
            return items
        finally:
            db.close()

    @blp.arguments(CreateExperimentRequest, location="json")
    @blp.response(201, ExperimentSchema, description="Created experiment")
    def post(self, payload):
        """Create a new experiment."""
        db = get_session()
        try:
            exp = repo.create_experiment(
                db,
                name=payload.get("name"),
                description=payload.get("description"),
                status=payload.get("status", "draft"),
            )
            return exp
        finally:
            db.close()

@blp.route("/<int:experiment_id>")
class ExperimentDetail(MethodView):
    """Get, update, delete an experiment."""

    @blp.response(200, ExperimentWithStepsSchema, description="Experiment with steps")
    def get(self, experiment_id: int):
        """Retrieve experiment with its steps."""
        db = get_session()
        try:
            result = repo.get_experiment_with_steps(db, experiment_id)
            if result is None:
                abort(404, description="Experiment not found")
            exp, steps = result
            # Attach steps for schema
            exp.steps = steps
            return exp
        finally:
            db.close()

    @blp.arguments(UpdateExperimentRequest, location="json")
    @blp.response(200, ExperimentSchema, description="Updated experiment")
    def patch(self, payload, experiment_id: int):
        """Update an experiment."""
        db = get_session()
        try:
            exp = repo.update_experiment(
                db,
                experiment_id=experiment_id,
                name=payload.get("name"),
                description=payload.get("description"),
                status=payload.get("status"),
            )
            if exp is None:
                abort(404, description="Experiment not found")
            return exp
        finally:
            db.close()

    @blp.response(204, description="Deleted")
    def delete(self, experiment_id: int):
        """Delete an experiment and its steps."""
        db = get_session()
        try:
            ok = repo.delete_experiment(db, experiment_id)
            if not ok:
                abort(404, description="Experiment not found")
            return ""
        finally:
            db.close()

@blp.route("/<int:experiment_id>/steps")
class ExperimentSteps(MethodView):
    """List and create steps for an experiment."""

    @blp.response(200, ExperimentWithStepsSchema, description="Experiment and steps")
    def get(self, experiment_id: int):
        """Get experiment with its steps."""
        db = get_session()
        try:
            result = repo.get_experiment_with_steps(db, experiment_id)
            if result is None:
                abort(404, description="Experiment not found")
            exp, steps = result
            exp.steps = steps
            return exp
        finally:
            db.close()
