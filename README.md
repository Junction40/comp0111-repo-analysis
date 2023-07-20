# Repository Comment Analyser

This script has been created to analyse repositories where a GitHub comment creation tool will be used.

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

For this example, we will use the PyGithub Repository. This repository is hosted on public GitHub.

1. Navigate to the `config.py` file in the repository.

2. Ensure the `github_enterprise_repo` variable is set to `False`. The `github_enterprise_hostname` variable will not be used in this case, and thus can be set to any value (e.g. `""`).

3. Set the `analysed-repository` value to the repository you want to analyse in the format of `"*USER_NAME*/*REPO_NAME*"`. For the example described at the beginning of this section, this value would be `"PyGithub/PyGithub"`.

4. In the `results` directory, create a file named `results_*REPO_NAME*.csv` with only the name of the repo you wish to analyse. For the example above, this would be `results_PyGithub.csv`.

5. You can now run the `comment-analysis-script.py` to see your results.

## Enterprise GitHub Repositories

For repositories hosted on an GitHub enterprise with a custom hostname, there is a slightly different process including an additional step compared to public repositories.

1. Navigate to the `config.py` file in the repository.

2. Ensure the `github_enterprise_repo` variable is set to `True`.

3. Ensure the `github_enterprise_hostname` variable is set to the hostname of your company's GitHub Enterprise (e.g. `"https://{hostname}"`)

4. You have now completed all enterprise-specific steps. Follow steps 3-5 of the [Public GitHub Repositories](#public-github-repositories) section to get the script running!
