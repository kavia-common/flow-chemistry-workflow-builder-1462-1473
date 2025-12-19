#!/bin/bash
cd /home/kavia/workspace/code-generation/flow-chemistry-workflow-builder-1462-1473/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

