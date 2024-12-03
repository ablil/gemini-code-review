#!/usr/bin/env python3

import os

def assert_env_variable(key: str, default_value: str|None = None) -> str:
    if not default_value:
        assert key in os.environ and len(os.environ[key].strip()), f"Missing env variable {key}"
    return os.environ[key] if key in os.environ and len(os.environ[key]) else default_value