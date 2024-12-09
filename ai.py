#!/usr/bin/env python3

from utils import assert_env_variable, create_logger, get_default_prompt

import google.generativeai as genai


logger = create_logger(__name__)

class Gemini:
    def __init__(self, apikey: str, extra_prompt: str|None = None, gemini_model: str = 'gemini-1.5-flash'):
        if extra_prompt:
            self.__prompt = f"""{get_default_prompt()}\n\n{extra_prompt}\n\nHere is the diff"""
        else:
            self.__prompt = f"""{get_default_prompt()}\n\nHere is the diff"""
            
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel(gemini_model)
        logger.info(f"Gemini client configured successfully with model '{gemini_model}'")
        logger.debug(f"using prompt '''{self.__prompt}'''")

    def ask(self, query: str) -> str:
        return self.model.generate_content(query).text

    def review(self, git_diff: str):
        logger.debug(f"Asking Gemini to review {git_diff[0:100]}")
        return self.model.generate_content(f"{self.__prompt}\n\n{git_diff}").text


if __name__ == '__main__':
    api_key = assert_env_variable('GEMINI_API_KEY')
    model = assert_env_variable('GEMINI_MODEL', 'gemini-1.5-flash')

    gemini = Gemini(api_key)
    print(gemini.ask('How can you help me ?'))
