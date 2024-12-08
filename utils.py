#!/usr/bin/env python3

import os

def get_files_from_gitignore(filename: str) -> list[str]:
    assert os.path.exists(filename), f"File {filename} not found"
    with open(filename, 'r') as f:
        lines = [line.strip() for line in  f.readlines()]
        return list(filter(lambda item: not item.startswith('#'), lines))


def assert_env_variable(key: str, default_value: str|None = None) -> str:
    if not default_value:
        assert key in os.environ and len(os.environ[key].strip()), f"Missing env variable {key}"
    return os.environ[key] if key in os.environ and len(os.environ[key]) else default_value

def get_env_variable_or_default(key: str, default_value = None):
    if key in os.environ:
        return os.environ[key].strip()

    return default_value
