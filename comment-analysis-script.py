# Import PyGithub
from github import Github
from github import Auth

SUGGEST_START = "```suggestion"
SUGGEST_END = "```"

# Import CSV Package
import csv

# Import config.py
import config

# *CHANGE VALUE TO NAME OF REPOSITORY TO ANALYSE*
analysed_repository = "PyGithub/PyGithub"

# Filename to store analysis results
results_filename = "results/results_{}.csv".format(analysed_repository.split("/")[1])

# Header for CSV results file
header = ["repo", "prID", "comment"]

# Add header row to the results file
with open(results_filename, "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(header)

# Define auth using access token from config.py
auth = Auth.Token(config.github_access_token)

# Define Github object
g = Github(auth=auth)

# # ** Uncomment the following 2 lines and comment the 2 lines above when testing on BBGithub. **
# # Define Github Enterprise object
# g = Github(auth=auth, base_url="https://{hostname}/api/v3")

# Fetch specific repository
repo = g.get_repo(analysed_repository)

# Get pull requests
pull_requests = repo.get_pulls()

# Get all comments from all pull requests
for pr in pull_requests:
    for comment in pr.get_comments():
        print(comment)
