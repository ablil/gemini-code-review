# Ask Gemini AI to Review Your Pull Requests

This GitHub Action integrates with **Gemini AI** to review your pull requests, providing insightful feedback to improve code quality and adherence to best practices.

## Features
- Automatically sends your pull request changes to Gemini AI for review.
- Ensures your code is well-structured and meets your quality standards.
- Seamlessly integrates into your CI/CD workflow.

## Inputs

| Input Name            | Required | Description                                                                                   |
|-----------------------|----------|-----------------------------------------------------------------------------------------------|
| `gemini_api_key`      | Yes      | Your Gemini API key. [Get your API key here](https://ai.google.dev/gemini-api/docs/api-key).  |
| `github_token`        | No       | A GitHub token for accessing the repository.                                                 |
| `github_repository`   | No       | The repository name, in the format `owner/repository`.                                       |
| `github_ref_name`     | No       | The pull request reference name (e.g., branch or tag name).                                  |

## Output

This action does not produce outputs but logs the feedback directly in the workflow run logs.

## Usage

Add the following to your workflow YAML file:

```yaml
name: Gemini AI Pull Request Review

on:
  pull_request:
    types: [opened]

jobs:
  gemini-review:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Gemini AI Review
        uses: your-username/your-action-repo@v1
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_repository: ${{ github.repository }}
          github_ref_name: ${{ github.ref_name }}

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
