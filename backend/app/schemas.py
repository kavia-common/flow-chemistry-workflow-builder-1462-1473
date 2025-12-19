from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class StepSchema(Schema):
    """Schema for Step object."""
    id = fields.Int(dump_only=True, description="Step ID")
    experiment_id = fields.Int(required=True, description="Parent Experiment ID")
    name = fields.Str(required=True, validate=validate.Length(min=1), description="Step name")
    type = fields.Str(required=False, allow_none=True, description="Step type/category")
    order_index = fields.Int(required=False, load_default=0, description="Ordering index within experiment")
    notes = fields.Str(required=False, allow_none=True, description="Optional notes for the step")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# PUBLIC_INTERFACE
class ExperimentSchema(Schema):
    """Schema for Experiment object."""
    id = fields.Int(dump_only=True, description="Experiment ID")
    name = fields.Str(required=True, validate=validate.Length(min=1), description="Experiment name")
    description = fields.Str(required=False, allow_none=True, description="Experiment description")
    status = fields.Str(required=False, load_default="draft", validate=validate.OneOf(["draft","running","completed","failed"]), description="Experiment status")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# PUBLIC_INTERFACE
class ExperimentWithStepsSchema(ExperimentSchema):
    """Schema for Experiment with embedded steps."""
    steps = fields.List(fields.Nested(StepSchema), dump_only=True)

# PUBLIC_INTERFACE
class CreateExperimentRequest(Schema):
    """Payload to create experiment."""
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False, load_default="draft")

# PUBLIC_INTERFACE
class UpdateExperimentRequest(Schema):
    """Payload to update experiment."""
    name = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False)

# PUBLIC_INTERFACE
class CreateStepRequest(Schema):
    """Payload to create step."""
    name = fields.Str(required=True)
    type = fields.Str(required=False, allow_none=True)
    order_index = fields.Int(required=False, load_default=0)
    notes = fields.Str(required=False, allow_none=True)

# PUBLIC_INTERFACE
class UpdateStepRequest(Schema):
    """Payload to update step."""
    name = fields.Str(required=False)
    type = fields.Str(required=False, allow_none=True)
    order_index = fields.Int(required=False)
    notes = fields.Str(required=False, allow_none=True)
