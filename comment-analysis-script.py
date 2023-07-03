# Import PyGithub
from github import Github
from github import Auth

# Import config.py
import config

# Define auth using access token from config.py
auth = Auth.Token(config.github_access_token)

# Define Github object
g = Github(auth=auth)

# # ** Uncomment the following 2 lines and comment the 2 lines above when testing on BBGithub. **
# # Define Github Enterprise object
# g = Github(auth=auth, base_url="https://{hostname}/api/v3")

# Temporary test: print your repos
for repo in g.get_user().get_repos():
    print(repo.name)
