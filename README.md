# Ask Gemini AI to Review Your Pull Requests

This GitHub Action integrates with **Gemini AI** to review your pull requests, providing insightful feedback to improve code quality and adherence to best practices.

## Features
- Automatically sends your pull request changes to Gemini AI for review.
- Ensures your code is well-structured and meets your quality standards.
- Seamlessly integrates into your CI/CD workflow.

## Inputs

| Input Name          | Required | Description                                                                                   |
|---------------------|----------|-----------------------------------------------------------------------------------------------|
| `GITHUB_TOKEN`      | Yes      | Github Token to interact with Github API, provided by google through ${{ secrets.GITHUB_TOKEN }} |
| `gemini_api_key`    | Yes      | Your Gemini API key. [Get your API key here](https://ai.google.dev/gemini-api/docs/api-key).  |
| `gemini_model`      | No       | The Gemini model to use, by default it's **gemini-1.5-flash**, you can find all models [here](https://ai.google.dev/gemini-api/docs/models/gemini) |
| `exclude_fileanems` | No       | Filenames patterns to exclude, default: '*.txt,*.yaml,*.yml,package-lock.json,yarn.lock |

## Output

This action does not produce outputs but logs the feedback directly in the workflow run logs.

## Usage

Add the following to your workflow YAML file:

```yaml
name: Gemini AI Pull Request Review

on:
  pull_request:

permissions: write-all

jobs:
  gemini-review:
    runs-on: ubuntu-latest

    steps:
      - name: Run Gemini AI Review
        uses: ablil/gemini-code-review@0.2.11
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Secrets

* **GEMINI_API_KEY**: Required to authenticate with Gemini AI
* **GITHUB_TOKEN**: Provided by GitHub for accessing the repository

### Setup

1. Obtain your Gemini API from [here]()
2. Add the API key as a repository secret:
   * Go to **Settings** >> **secrets and variables** >> **actions** >> **New repository secret**
   * Name it **GEMINI_API_KEY** and paste your key.
3. Update your workflow with the example above.
