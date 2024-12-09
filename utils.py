#!/usr/bin/env python3

import os
import logging

def is_debug_enabled() -> bool:
    return 'DEBUG' in os.environ and os.environ['DEBUG'].strip().lower() in ['1', 'true']

logging.basicConfig(level=logging.DEBUG if is_debug_enabled() else logging.INFO)

def get_files_from_gitignore(filename: str) -> list[str]:
    assert os.path.exists(filename), f"File {filename} not found"
    with open(filename, 'r') as f:
        lines = [line.strip() for line in  f.readlines()]
        return list(filter(lambda item: not item.startswith('#'), lines))


def assert_env_variable(key: str, default_value: str|None = None) -> str:
    if not default_value:
        assert key in os.environ and len(os.environ[key].strip()), f"Missing env variable {key}"

    if key in os.environ and len(os.environ[key].strip()):
        return os.environ[key].strip()

    logging.warning(f"Missing env variable '{key}', using default value '{default_value}' instead")
    return default_value

def get_env_variable_or_default(key: str, default_value = None):
    if key in os.environ:
        return os.environ[key].strip()

    logging.warning(f"Missing env variable '{key}', using default value '{default_value}' instead")
    return default_value

def create_logger(name: str = __name__) -> bool:
    logger = logging.getLogger(name)

    is_debug =  'DEBUG' in os.environ and os.environ['DEBUG'].strip().lower() in ['1', 'true']
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    return logger

def get_default_prompt(filename: str = 'prompt.txt') -> str:
    with open(filename, 'r') as f:
        return f.read().strip()
