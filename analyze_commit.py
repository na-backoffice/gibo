import os
import subprocess
from openai import OpenAI
import requests

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ.get("PR_NUMBER")
COMMIT_SHA = os.environ.get("COMMIT_SHA")

def get_commit_message():
    return subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode().strip()

def gpt_feedback(message):
    prompt = f"""Du bist ein hilfreicher Code-Coach. Analysiere die folgende Commit-Message und gib konstruktives, eventuell humorvolles Feedback (max. 3 kurze Bullet-Points). Nutze auch Emojis.

Commit-Message:
\"\"\"
{message}
\"\"\"
"""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def comment_on_pr(feedback):
    if not PR_NUMBER:
        print("Kein Pull Request erkannt.")
        return
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": f"🤖 Commit-Coach sagt:\n\n{feedback}"}
    response = requests.post(url, headers=headers, json=data)
    print("Kommentar gepostet:", response.ok)


if __name__ == "__main__":
    commit_msg = get_commit_message()
    feedback = gpt_feedback(commit_msg)
    print("GPT Feedback:\n", feedback)
    comment_on_pr(feedback)
