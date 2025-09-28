import json
import re

PR_STATE_MARKER = "<!-- GEMINI_REVIEWED_HASHES -->"

# These functions assume the PR object is a PyGithub PullRequest


def get_state_comment(pr):
    """Return (comment, content) for the state marker, or (None, None) if not found."""
    for c in pr.get_issue_comments():
        if c.body and c.body.startswith(PR_STATE_MARKER):
            try:
                data = json.loads(c.body[len(PR_STATE_MARKER):].strip())
                return c, data
            except Exception:
                continue
    return None, {"reviewed_hashes": {}, "last_reviewed_sha": None}

def upsert_state_comment(pr, state):
    """Create or update the state marker comment on the PR."""
    import json
    body = PR_STATE_MARKER + "\n" + json.dumps(state)
    comment, _ = get_state_comment(pr)
    if comment:
        comment.edit(body)
    else:
        pr.create_issue_comment(body)
