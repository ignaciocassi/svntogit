import os
import urllib
from urllib import request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


def prompt_subversion_server_credentials():
    subversion_server_credentials = \
        {"subversion_url": input("[*] Please enter the URL address for target Subversion server: "),
         "subversion_username": input("[*] Please enter the username for authenticating in Subversion server: "),
         "subversion_password": input("[*] Please enter the password authenticating in Subversion server: ")}
    return subversion_server_credentials


def get_subversion_server_response(subversion_server_credentials):
    url_opener, svn_request = get_url_opener_and_request(subversion_server_credentials)
    try:
        result = url_opener.open(svn_request)
        response = result.read()
        return response
    except HTTPError:
        print("\n[X] The username, password or URL entered are incorrect please try again...\n")
        prompt_subversion_server_credentials()
    except URLError:
        print("\n[X] The URL entered is incorrect or inaccessible, please try again...\n")
        prompt_subversion_server_credentials()


def get_url_opener_and_request(subversion_server_credentials):
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None,
                                  subversion_server_credentials["subversion_url"],
                                  subversion_server_credentials["subversion_username"],
                                  subversion_server_credentials["subversion_password"])
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    url_opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(url_opener)
    svn_request = urllib.request.Request(subversion_server_credentials["subversion_url"])
    return url_opener, svn_request


def parse_response_to_repo_list(response):
    soup = BeautifulSoup(response, features="html.parser")
    repos = [a.text.replace("/", "") for a in soup.findAll('a') if a.text != "Subversion"]
    return repos


def migrate_repositories(repos, subversion_server_credentials):
    correct_repos = []
    incorrect_repos = []
    repo_counter = 0

    for repo in repos:
        status_codes = []

        subgit_configure = "subgit configure " + subversion_server_credentials["subversion_url"] + repo + "/"
        run_command(subgit_configure, status_codes)

        append_credentials_to_passwd_file(os.getcwd()
                                          + "\\"
                                          + repo
                                          + ".git"
                                          + "\\subgit\\passwd",
                                          subversion_server_credentials)

        subgit_install = "subgit install " + repo + ".git"
        run_command(subgit_install, status_codes)

        kill_subgit_install_trash_process = "taskkill /f /im java.exe"
        run_command(kill_subgit_install_trash_process, status_codes)

        git_clone = "git clone " + repo + " " + repo + "-GIT.git"
        run_command(git_clone, status_codes)

        rmdir_trash = "rmdir /s /q " + repo + ".git"
        run_command(rmdir_trash, status_codes)

        if all(code == 0 for (code) in status_codes):
            correct_repos.append(subversion_server_credentials["subversion_url"] + repo)
        else:
            incorrect_repos.append(subversion_server_credentials["subversion_url"] + repo)

        repo_counter += 1

    return correct_repos, incorrect_repos


def run_command(command, status_codes):
    print("\n[*] " + command)
    status_code = os.system(command)
    status_codes.append(status_code)


def append_credentials_to_passwd_file(passwd_file_path, subversion_server_credentials):
    with open(passwd_file_path, "wt") as file:
        file.write(subversion_server_credentials["subversion_username"]
                   + " " +
                   subversion_server_credentials["subversion_password"])


def show_repo_migration_results(subversion_server_credentials, total_repos, correct_repos, incorrect_repos):
    print("\n[*] The migration process ended. "
          + str(total_repos) + " Were processed, "
          + str(len(correct_repos)) + " were correct, and "
          + str(len(incorrect_repos)) + " had errors.")

    print("\n[✓] Correct repositories: ")
    for correct_repo in correct_repos:
        print(correct_repo)
    save_to_file("correct_repos", correct_repos)

    print("\n[x] Incorrect repositories: ")
    for correct_repo in correct_repos:
        print(correct_repo)
    save_to_file("incorrect_repos", incorrect_repos)


def save_to_file(file_name, repo_list):
    with open(file_name, "wt") as file:
        for repo in repo_list:
            file.write(repo + "\n")


def __main__():
    # TODO: Make dict() global to avoid multiple argument passes.
    # TODO: Make final .git repository folder have "repo.git" format as a name.
    subversion_server_credentials = prompt_subversion_server_credentials()
    response = get_subversion_server_response(subversion_server_credentials)
    repo_list = parse_response_to_repo_list(response)
    correct_repos, incorrect_repos = migrate_repositories(repo_list, subversion_server_credentials)
    show_repo_migration_results(subversion_server_credentials, len(repo_list), correct_repos, incorrect_repos)


if __name__ == "__main__":
    __main__()
