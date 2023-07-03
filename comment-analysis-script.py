# Import PyGithub
from github import Github
from github import Auth

# Import CSV Package
import csv

# Import config.py
import config

analysed_repository = "PyGithub/PyGithub"

# Define auth using access token from config.py
auth = Auth.Token(config.github_access_token)

# Define Github object
g = Github(auth=auth)

# # ** Uncomment the following 2 lines and comment the 2 lines above when testing on BBGithub. **
# # Define Github Enterprise object
# g = Github(auth=auth, base_url="https://{hostname}/api/v3")

# # Temporary test: print your repos
# for repo in g.get_user().get_repos():
#     print(repo.name)

# Fetch specific repository
repo = g.get_repo(analysed_repository)

# Get pull requests
pull_requests = repo.get_pulls()

# Get all comments from all pull requests
for pr in pull_requests:
    for comment in pr.get_comments():
        print(comment)
