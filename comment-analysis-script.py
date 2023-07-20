# Import PyGithub
from github import Github
from github import Auth

SUGGEST_START = "```suggestion"
SUGGEST_END = "```"

# Import CSV Package
import csv
import datetime

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
        comment.user.login == "B-Assist"
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
            snippet[len(SUGGEST_START) : end - len(SUGGEST_END)]
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


def check_comment_action(comment, pr):
    # Check if the comment was accepted/rejected/ignored
    if pr.commits > 1:
        for commit in pr.get_commits():
            if (
                comment.path in [f.filename for f in commit.files]
                and commit.commit.committer.date > comment.created_at
            ):
                return commit
    return "Ignored/Rejected"


def main():
    # Add header row to the results file
    with open(results_filename, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(header)

    # Define auth using access token from config.py
    auth = Auth.Token(credentials.github_access_token)

    if config.github_enterprise_repo:
        g = Github(
            auth=auth, base_url=("{}/api/v3".format(config.github_enterprise_hostname))
        )
    else:
        g = Github(auth=auth)

    # Fetch specific repository
    repo = g.get_repo(config.analysed_repository)

    # Get pull requests
    pull_requests = repo.get_pulls()

    # Get all comments from all pull requests
    for pr in pull_requests:
        for comment in pr.get_comments():
            # Run analysis methods
            is_suggestion = check_is_suggestion(comment)
            bassist_comment = check_bassist(comment)
            comment_text, comment_code = extract_code_and_body(comment, is_suggestion)
            comment_action = "-"
            reaction_time = "No Reaction"
            if is_suggestion and comment_action != "Ignored/Rejected" and "-":
                comment_action = check_comment_action(comment, pr)
                # If the comment is a suggestion and accepted, check reaction time from comment creation to commit in total seconds
                if comment_action != "Ignored/Rejected" and "-":
                    reaction_time = (
                        comment_action.commit.committer.date - comment.created_at
                    ).total_seconds()
                    # Since there is a commit object, just make it accepted for the csv
                    comment_action = "Accepted"

            # Create row to be added to CSV file
            row = [
                pr.base.repo.full_name.encode("utf-8"),  # Repo name
                pr.number,  # PR ID
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
