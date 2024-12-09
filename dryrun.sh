#!/bin/bash

export DRY_RUN=true
export DEBUG=true
export GITHUB_REF_NAME=5/foo/bar
export GITHUB_REPOSITORY=ablil/gemini-code-review
export EXTRA_PROMPT="Ignore all changes about import sorting, or code formatting"

python app.py
