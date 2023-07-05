# Import PyGithub
from github import Github
from github import Auth

SUGGEST_START = "```suggestion"
SUGGEST_END = "```"

# Import CSV Package
import csv
import datetime

# Import config.py
import config

# *CHANGE VALUE TO NAME OF REPOSITORY TO ANALYSE*
analysed_repository = "PyGithub/PyGithub"

# Filename to store analysis results
results_filename = "results/results_{}.csv".format(analysed_repository.split("/")[1])

# Header for CSV results file
header = [
    "repo",  # Repo Name
    "prID",  # Pull Request ID
    "b-assist-comment",  # Was the comment created by B-Assist?
    "comment",  # Comment Contents
    "suggestion",  # Was the comment a suggestion?
    "action",  # How did the reviewer react to the comment? (Accept, Reject, Ignore)
    "response_time",  # How much time elapsed between when the comment was created and when the reviewer reacted to it.
]

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

# header = [
#     "repo",  # Repo Name
#     "prID",  # Pull Request ID
#     "b-assist-comment",  # Was the comment created by B-Assist?
#     "comment",  # Comment contents
#     "suggestion",  # Was the comment a suggestion?
#     "action",  # How did the developer react to the comment? (Accept, Reject, Ignore)
#     "response_time"
# ]

# Get all comments from all pull requests
for pr in pull_requests:
    for comment in pr.get_comments():
        response_time = comment.created_at
        print("Reading Comment")
        row = [
            pr.base.repo.full_name.encode("utf-8"),  # Repo name
            pr.number,  # PR ID
            "false",  # Change to check if B-Assist created the comment
            comment.body.encode("utf-8"),  # Comment Body
            "false",  # Change to check if the comment is a suggestion
            "accepted",  # Change to check if the comment was accepted/rejected/ignored
            datetime.datetime.now(),  # Change to calculation of response time
        ]
        with open(results_filename, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(row)
