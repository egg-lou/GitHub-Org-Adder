from github import Github
from github.GithubException import UnknownObjectException, GithubException
import csv
from dotenv import load_dotenv
import os
import json

load_dotenv()

def add_members_to_organization(csv_file_path):
    github_token = os.getenv("GITHUB_TOKEN")
    organization_name = os.getenv("ORGANIZATION_NAME")

    g = Github(github_token)

    try:
        org = g.get_organization(organization_name)
    except UnknownObjectException as e:
        print(f"Organization {organization_name} not found. Error: {str(e)}")
        return
    except GithubException as e:
        print(f"Failed to retrieve organization {organization_name}. Error: {str(e)}")
        return

    added_members = []

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row.get('username', '')
            role = row.get('role', '')

            if not username:
                print("Skipping row. No username provided.")
                continue

            try:
                existing_members = [member.login for member in org.get_members()]
                if username in existing_members:
                    print(f"{username} is already a member of the organization.")
                    continue

                user = g.get_user(username)

                if role.lower() == 'admin':
                    org.add_to_members(user, role='admin')
                else:
                    org.add_to_members(user, role='member')

                added_members.append({"username": username, "role": role})
                print(f"Added {username} as {role} to the organization.")
            except GithubException as e:
                print(f"Failed to add {username} to {organization_name} with role {role}. Error: {str(e)}")

    added_members_json = json.dumps(added_members, indent=2)
    print("\nAdded Members:")
    print(added_members_json)

if __name__ == "__main__":
    csv_file_path = "done.csv"

    add_members_to_organization(csv_file_path)
