from github import Github
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_organization_members():
    github_token = os.getenv("GITHUB_TOKEN")
    organization_name = os.getenv("ORGANIZATION_NAME")

    g = Github(github_token)

    try:
        org = g.get_organization(organization_name)
    except Exception as e:
        print(f"Failed to retrieve organization {organization_name}. Error: {str(e)}")
        return

    try:
        members = org.get_members()
        members_data = [{"username": member.login, "id": member.id} for member in members]

        json_output = json.dumps(members_data, indent=2)
        print(json_output)
    except Exception as e:
        print(f"Failed to retrieve members of {organization_name}. Error: {str(e)}")

if __name__ == "__main__":
    get_organization_members()
