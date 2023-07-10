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
    "pr_ID",  # Pull Request ID
    "bassist_comment",  # Was the comment created by B-Assist?
    "comment_text",  # Regular text in comment
    "comment_code",  # Suggested code in comment
    "suggestion",  # Was the comment a suggestion?
    "action",  # How did the reviewer react to the comment? (Accept, Reject, Ignore)
    "response_time",  # How much time elapsed between when the comment was created and when the reviewer reacted to it.
    # if the pr closed with the changes the pr is ignored
    # while pr is still opeen and hcanges haven been implented yet they're in the "unknown/waiting" phase
]


def check_bassist(comment):
    # Check if B-Assist created the comment
    return False


def check_is_suggestion(comment):
    # Check if the review comment is a suggestion
    return False


def extract_code_and_body(comment, suggestion):
    # Return separated code and comment contents

    # If there is a suggestion, there should be code.
    if suggestion == True:
        return "**Comment Text**", "**Code**"
    # If no suggestion, return the comment body and "No Code".
    else:
        return "**Comment Text**", "No Code"

def check_comment_action(comment, pr):
    # Check if the comment was accepted/rejected/ignored
    # print(comment.body)
    
    if pr.commits > 1:
        for commit in pr.get_commits():
            if (
                comment.path in [f.filename for f in commit.files]
                and commit.commit.committer.date > comment.created_at
            ):
                print(comment.path)
                return "accepted"
    return "ignored"


def check_reaction_time(comment):
    # If the comment was accepted or rejected, return the time of reaction - the time the comment was created
    return datetime.datetime.now()


def main():
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
            # print("Reading Comment")

            # Run analysis methods
            bassist_comment = check_bassist(comment)
            is_suggestion = check_is_suggestion(comment)
            comment_code, comment_text = extract_code_and_body(comment, is_suggestion)
            comment_action = check_comment_action(comment, pr)
            reaction_time = "No Reaction"
            if comment_action != "ignored":
                reaction_time = check_reaction_time(comment)

            # Create row to be added to CSV file
            row = [
                pr.base.repo.full_name.encode("utf-8"),  # Repo name
                pr.number,  # PR ID
                bassist_comment,  # Change to check if B-Assist created the comment
                comment_text,  # Text in comment
                comment_code,  # Suggested code in comment
                is_suggestion,  # Change to check if the comment is a suggestion
                comment_action,  # Change to check if the comment was accepted/rejected/ignored
                reaction_time,  # Change to calculation of response time
            ]
            with open(results_filename, "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(row)


if __name__ == "__main__":
    main()
