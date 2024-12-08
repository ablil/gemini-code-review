#!/bin/bash

export DRY_RUN=true
export GITHUB_REF_NAME=5/foo/bar
export GITHUB_REPOSITORY=ablil/gemini-code-review

root_dir=$(git rev-parse --show-toplevel)
python $root_dir/src/app.py
