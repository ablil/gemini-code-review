#!/usr/bin/env python3

import logging

import google.generativeai as genai
from utils import assert_env_variable
logging.basicConfig(level=logging.DEBUG)

class Gemini:
    __prompt = """
Review only the changes in the following git diff and provide clear, concise suggestions for improvement. Focus on aspects like readability, performance, and maintainability in the changed code. Include code samples or refactor suggestions where applicable. Do not review the unchanged code, and avoid unnecessary explanations—just actionable feedback on the modifications. Here’s the diff:"""

    def __init__(self, apikey: str, gemini_model: str = 'gemini-1.5-flash'):
        genai.configure(api_key=apikey)
        logging.info("Gemini client configured successfully")
        self.model = genai.GenerativeModel(gemini_model)

    def ask(self, query: str) -> str:
        logging.info(f"Asking Gemini {query[0:50]}")
        return self.model.generate_content(query).text

    def review(self, git_diff: str):
        logging.debug(f"Asking Gemini to review {git_diff[0:50]}")
        return self.model.generate_content(f"{self.__prompt}\n\n{git_diff}").text


if __name__ == '__main__':
    api_key = assert_env_variable('GEMINI_API_KEY')
    model = assert_env_variable('GEMINI_MODEL', 'gemini-1.5-flash')

    gemini = Gemini(api_key, model)
    print(gemini.ask('How can you help me ?'))
