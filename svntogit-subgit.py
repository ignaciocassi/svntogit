import os
import urllib
from urllib import request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


def prompt_subversion_server_credentials(subv_server):
    subv_server["url"] = input("[*] Please enter the URL address for target Subversion server: ")
    subv_server["username"] = input("[*] Please enter the username for authenticating in Subversion server: ")
    subv_server["password"] = input("[*] Please enter the password authenticating in Subversion server: ")
    return subv_server, get_subversion_server_response(subv_server)


def get_subversion_server_response(subv_server):
    try:
        url_opener, svn_request = get_url_opener_and_request(subv_server)
        result = url_opener.open(svn_request)
        response = result.read()
        return response
    except HTTPError:
        print("\n[X] The username, password or URL entered are incorrect please try again...\n")
        prompt_subversion_server_credentials(subv_server)
    except URLError:
        print("\n[X] The URL entered is incorrect or inaccessible, please try again...\n")
        prompt_subversion_server_credentials(subv_server)
    except ValueError:
        print("\n[X] The URL entered is incorrect or inaccessible, please try again...\n")
        prompt_subversion_server_credentials(subv_server)


def get_url_opener_and_request(subv_server):
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None,
                                  subv_server["url"],
                                  subv_server["username"],
                                  subv_server["password"])
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    url_opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(url_opener)
    svn_request = urllib.request.Request(subv_server["url"])
    return url_opener, svn_request


def parse_response_to_repo_list(response):
    soup = BeautifulSoup(response, features="html.parser")
    repos = [a.text.replace("/", "") for a in soup.findAll('a') if a.text != "Subversion"]
    return repos


def migrate_repositories(repos, subv_server):
    correct_repos = []
    incorrect_repos = []
    repo_counter = 0

    for repo in repos:
        status_codes = []

        subgit_configure = "subgit configure " + subv_server["url"] + repo + "/"
        run_command(subgit_configure, status_codes)

        append_credentials_to_passwd_file(os.getcwd()
                                          + "\\"
                                          + repo
                                          + ".git"
                                          + "\\subgit\\passwd",
                                          subv_server)

        subgit_install = "subgit install " + repo + ".git"
        run_command(subgit_install, status_codes)

        kill_subgit_install_trash_process = "taskkill /f /im java.exe"
        run_command(kill_subgit_install_trash_process, status_codes)

        git_clone = "git clone " + repo + " " + repo + "-temp.git"
        run_command(git_clone, status_codes)

        rmdir_trash = "rmdir /s /q " + repo + ".git"
        run_command(rmdir_trash, status_codes)

        rename_folder = "ren " + repo + "-temp.git " + repo + ".git"
        run_command(rename_folder, status_codes)

        if all(code == 0 for (code) in status_codes):
            correct_repos.append(subv_server["url"] + repo)
        else:
            incorrect_repos.append(subv_server["url"] + repo)

        repo_counter += 1

    return correct_repos, incorrect_repos


def run_command(command, status_codes):
    print("\n[*] " + command)
    status_code = os.system(command)
    status_codes.append(status_code)


def append_credentials_to_passwd_file(passwd_file_path, subv_server):
    with open(passwd_file_path, "wt") as file:
        file.write(subv_server["username"]
                   + " " +
                   subv_server["password"])


def show_repo_migration_results(total_repos, correct_repos, incorrect_repos):
    print("\n[*] The migration process ended. "
          + str(total_repos) + " Were processed, "
          + str(len(correct_repos)) + " were correct, and "
          + str(len(incorrect_repos)) + " had errors.")

    if len(correct_repos) > 0:
        print("\n[✓] Correct repositories: ")
        for correct_repo in correct_repos:
            print(correct_repo)
        save_to_file("correct_repos", correct_repos)

    if len(incorrect_repos) > 0:
        print("\n[x] Incorrect repositories: ")
        for incorrect_repo in incorrect_repos:
            print(incorrect_repo)
        save_to_file("incorrect_repos", incorrect_repos)


def save_to_file(file_name, repo_list):
    with open(file_name, "wt") as file:
        for repo in repo_list:
            file.write(repo + "\n")


def __main__():
    # TODO: Make the script executable with arguments for Subversion server credentials.
    subv_server = dict()
    subv_server, response = prompt_subversion_server_credentials(subv_server)
    repo_list = parse_response_to_repo_list(response)
    correct_repos, incorrect_repos = migrate_repositories(repo_list, subv_server)
    show_repo_migration_results(len(repo_list), correct_repos, incorrect_repos)


if __name__ == "__main__":
    __main__()
