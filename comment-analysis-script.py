# Import PyGithub
from github import Github
from github import Auth
import urllib

SUGGEST_START = "```suggestion" # "```suggestion\r\n"
SUGGEST_END = "```"

# Import CSV Package
import csv
from datetime import datetime

# Import config.py
import credentials, config

# TODO
# If the pr closed with the changes the pr is ignored
# While pr is still open and changes haven't been implemented yet, they're in the "unknown/waiting" phase

# Filename to store analysis results
results_filename = "results/results_{}.csv".format(
    config.analysed_repository.split("/")[1]
)

# Header for CSV results file
header = [
    "repo",  # Repo Name
    "pr_ID",  # Pull Request ID
    "creation_date", # Comment creation date
    "suggestion",  # Was the comment a suggestion?
    "bassist_comment",  # Was the comment created by B-Assist?
    "comment_text",  # Regular text in comment
    "comment_code",  # Suggested code in comment
    "action",  # How did the reviewer react to the comment? (Accept, Reject, Ignore)
    "response_time",  # How much time elapsed between when the comment was created and when the reviewer reacted to it.
    "url",  # URL to comment
]


def check_bassist(comment):
    # Check if B-Assist created the comment
    return (
        comment.user.login == "fixie"
    )  # TODO: Update based on final decided username


def check_is_suggestion(comment):
    # Check if the review comment is a suggestion
    return SUGGEST_START in comment.body


def extract_code_and_body(comment, suggestion):
    # Return separated code and comment contents

    # If there is a suggestion, there should be code.
    if suggestion == True:
        # Starting index of code suggestion (including "```suggestion")
        start = comment.body.index(SUGGEST_START)

        # Ending index of code suggestion (search starting after found snippet start index, including "```")
        end = comment.body.index(SUGGEST_END, start + len(SUGGEST_START)) + len(
            SUGGEST_END
        )

        # Suggestion code snippet (including suggestion prefix and suffix)
        snippet = comment.body[start:end]

        # Formatted code snippet with the suggestion prefix and suffix removed
        formatted_snippet = (
            snippet[len(SUGGEST_START) : -len(SUGGEST_END)]
            .strip()
            .replace("\r", "")
            .encode("utf-8")
        )

        # Remove the code snippet from the original comment to leave only the regular text
        comment_text = (
            comment.body.replace(snippet, " - CODE - ")
            .replace("\r", "")
            .replace("\n", "")
            .encode("utf-8")
        )

        return comment_text, formatted_snippet
    # If no suggestion, return the comment body and "No Code".
    else:
        return comment.body.encode("utf-8"), "No Code"

def _wget(link):
    try:
        src = urllib.request.urlopen(link).read()
        # print(src)
    except urllib.error.HTTPError:
        print("ERROR: ", link)
        return ""
    return src

def check_comment_action(comment, pr, comment_code):
    # Check if the comment was accepted/rejected/ignored
    if pr.commits > 1:
        for commit in pr.get_commits():
            # Check if the comment is within a file of the commited files and the corresponding commit date is newer than the comment creation date
            if (
                comment.path in [f.filename for f in commit.files]
                and commit.commit.committer.date > comment.created_at
            ):
                file_url = (
                    commit.html_url.replace(
                        "github.com", "raw.githubusercontent.com"
                    ).replace("commit/", "")
                    + "/"
                    + comment.path
                )

                src = _wget(file_url)
                
                # Decode both bytes to compare as a string and check if the code snippet is within the commit's corresponding file
                if comment_code.decode("utf-8") in src.decode("utf-8"):
                    reaction_time = (
                    commit.commit.committer.date - comment.created_at
                    ).total_seconds()
                    return "Accepted", reaction_time
    return "Ignored/Rejected", "No Reaction"


def main():
    # Add header row to the results file
    with open(results_filename, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(header)

    # Define auth using access token from config.py
    auth = Auth.Token(credentials.github_access_token)

    if config.github_enterprise_repo:
        hostname = config.github_enterprise_hostname + "api/v3"
        g = Github(
            auth=auth, base_url=hostname
        )
    else:
        g = Github(auth=auth)

    # Fetch specific repository
    repo = g.get_repo(config.analysed_repository)

    # Get pull requests
    pull_requests = repo.get_pulls(state="all")

    comment_filter_date = datetime.strptime(config.filter_date, '%d/%m/%Y')

    # Get all comments from all pull requests
    for pr in pull_requests:
        for comment in pr.get_comments(sort='created', direction='desc'):
            print("Reading Comment")
            
            # Check if the current comment is older than the selected filter date
            if comment.created_at < comment_filter_date:
                print("Comment Skipped - Too Old")
                # Since comments are sorted chronologically for each PR, the first out of date comment 
                # for a PR means all following comments for that PR will also be out of date. Thus, we can use break.
                break

            # Run analysis methods
            is_suggestion = check_is_suggestion(comment)
            bassist_comment = check_bassist(comment)
            comment_text, comment_code = extract_code_and_body(comment, is_suggestion)
            comment_action = "-"
            reaction_time = "No Reaction"

            if is_suggestion:
                comment_action, reaction_time = check_comment_action(comment, pr, comment_code)

            # Create row to be added to CSV file
            row = [
                pr.base.repo.full_name.encode("utf-8"),  # Repo name
                pr.number,  # PR ID
                comment.created_at, # Comment creation date
                is_suggestion,  # Change to check if the comment is a suggestion
                bassist_comment,  # Change to check if B-Assist created the comment
                comment_text,  # Text in comment
                comment_code,  # Suggested code in comment
                comment_action,  # Change to check if the comment was accepted/rejected/ignored
                reaction_time,  # Change to calculation of response time
                comment.html_url,  # Comment URL
            ]
            with open(results_filename, "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(row)


if __name__ == "__main__":
    main()
