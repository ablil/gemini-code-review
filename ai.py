#!/usr/bin/env python3

import logging
import os

import google.generativeai as genai

logging.basicConfig(level=logging.DEBUG)

__prompt = """
Review only the changes in the following git diff and provide clear, concise suggestions for improvement. Focus on aspects like readability, performance, and maintainability in the changed code. Include code samples or refactor suggestions where applicable. Do not review the unchanged code, and avoid unnecessary explanations—just actionable feedback on the modifications. Here’s the diff:"""

def configure_credentials(api_key: str = os.environ['GEMINI_API_KEY']):
    assert len(api_key), 'invalid api key'
    logging.info("configuring credentials")
    genai.configure(api_key=api_key)

def __get_user_gemini_model_or_default() -> str:
    if 'GEMINI_MODEL' in os.environ and len(os.environ['GEMINI_MODEL']):
        return os.environ['GEMINI_MODEL']
    return 'gemini-1.5-flash'

def ask(git_diff: str) -> str:
    configure_credentials()
    logging.debug("Asking Gemini AI")
    model = genai.GenerativeModel(__get_user_gemini_model_or_default())
    response = model.generate_content(f"{__prompt}\n\n{git_diff}")
    return response.text
