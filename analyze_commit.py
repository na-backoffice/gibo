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
    prompt = f"""Du hast den Charakter und die Sprechweise von "Thomas Magnum". Du gibts Feedback zu einem Commit-Message. Fasse dich kurz und prägnant.

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
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": f"GICOBO sagt:\n\n{feedback}"}
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        print("Kommentar gepostet:", response.ok)
    else:
        print("Fehler beim Posten des Kommentars:", response.status_code, response.text)


if __name__ == "__main__":
    commit_msg = get_commit_message()
    feedback = gpt_feedback(commit_msg)
    print("GPT Feedback:\n", feedback)
    comment_on_pr(feedback)
