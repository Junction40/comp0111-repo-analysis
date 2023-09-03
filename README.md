# Repository Comment Analyser

This script has been created to analyse repositories where B-Assist will be used. It collects multiple pieces of data for each review comment made on a given repository.

For each comment, the script collects the following information and stores it in a CSV row:

- **repo**: The name of the repository where the comment was posted.
- **pr_ID**: The ID of the pull request to which the comment was posted.
- **creation_date**: The comment creation datetime.
- **suggestion**: Bool - Whether the comment contained a suggested change.
- **bassist_comment**: Bool - Whether the comment was created by B-Assist.
- **comment_text**: The extracted normal text from the comment.
- **comment_code**: The extracted code snippet from the comment (if any).
- **action**: The response to the comment. This field is determined by whether the code snippet from the comment appears in any of the commits made after the comment was posted in the pull request. This will either be "-" if the comment is not a suggestion, "Accepted" if the snippet is found in the later commits, and "Rejected/Ignored" otherwise.
- **response_time**: If the suggestion was accepted, this value is calculated as the time between the commit where the suggestion snippet appeared and when the comment was posted. Otherwise, it is "No Reaction".
- **url**: URL to access the comment directly.

# Setup & Authentication

1. Install the dependencies: `pip install -r requirements.txt`

2. Create a Github access token to use PyGithub.

3. Create a `credentials.py` file in the root directory and add a variable with a string value of the access token you've created:

#### **`credentials.py`**

```py
github_access_token = "*YOUR_ACCESS_TOKEN*"
```

# Using the Script

Before running the script, you need to decide which repository you want to analyse.

## Public GitHub Repositories

For this example, we will use the mock repository we created to test the script. This repository is hosted on public GitHub.

1. Navigate to the `config.py` file in the repository.

2. Ensure the `github_enterprise_repo` variable is set to `False`. The `github_enterprise_hostname` variable will not be used in this case, and thus can be set to any value (e.g. `""`).

3. Set the `analysed-repository` value to the repository you want to analyse in the format of `"*USER_NAME*/*REPO_NAME*"`. For the example described at the beginning of this section, this value would be `"davejjwilliams/repository-analysis-mock"`.

4. Set the `filter_date` variable to the date from which you want to save comments onwards. If you want to keep all comments, you can simply choose a reasonably old date that will encompass all commits since the beginning of the repository (e.g. 30 years ago). PLEASE NOTE: the format of the date is European with 4-digit year, e.g. 25/12/2000.

5. In the `results` directory, create a file named `results_*REPO_NAME*.csv` with only the name of the repo you wish to analyse. For the example above, this would be `results_repository-analysis-mock.csv`.

6. You can now run the `comment-analysis-script.py` to see your results.

## Enterprise GitHub Repositories

For repositories hosted on a GitHub enterprise with a custom hostname, there is a slightly different process including an additional step compared to public repositories.

1. Navigate to the `config.py` file in the repository.

2. Ensure the `github_enterprise_repo` variable is set to `True`.

3. Ensure the `github_enterprise_hostname` variable is set to the hostname of your company's GitHub Enterprise (e.g. `"https://{hostname}"`)

4. You have now completed all the enterprise-specific steps. Follow steps 3-6 of the [Public GitHub Repositories](#public-github-repositories) section to get the script running!

# Testing

Testing on this script has been conducted using the [davejjwilliams/repository-analysis-mock](https://github.com/davejjwilliams/repository-analysis-mock) repository. To ensure the script is functioning correctly, please follow the example described in the [Public GitHub Repositories](#public-github-repositories) section and check the output in your CSV file matches the mock repository's README.
