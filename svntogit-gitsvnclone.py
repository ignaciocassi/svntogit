import os
import urllib
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def prompt_subversion_server_credentials():
    subversion_url = input("[*] Please enter the URL address for target Subversion server: ")
    subversion_username = input("[*] Please enter the username for authenticating in Subversion server: ")
    subversion_password = input("[*] Please enter the password authenticating in Subversion server: ")
    return subversion_url, subversion_username, subversion_password


def get_url_opener_and_request(subversion_url, subversion_username, subversion_password):
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, subversion_url, subversion_username, subversion_password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    url_opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(url_opener)
    svn_request = urllib.request.Request(subversion_url)
    return url_opener, svn_request


def get_subversion_server_response(subversion_url, subversion_username, subversion_password):
    url_opener, svn_request = get_url_opener_and_request(subversion_url, subversion_username, subversion_password)
    try:
        result = url_opener.open(svn_request)
        response = result.read()
        return response
    except HTTPError:
        print("[X] The username, password or URL entered are incorrect please try again...\n")
        prompt_subversion_server_credentials()


def parse_response_to_repo_list(response):
    soup = BeautifulSoup(response, features="html.parser")
    repo_list = [a.text for a in soup.findAll('a')]
    return repo_list


def migrate_repositories(subversion_url, subversion_username, repo_list):
    print("\n[*] Attempting to migrate a total of " + str(len(repo_list)) + " repositories from SVN to GIT.\n")
    correct_repo_list = []
    incorrect_repo_list = []
    for i in range(1, len(repo_list)):
        counter = "[" + str(i) + "/" + str(len(repo_list)) + "] -> "
        command = "git svn clone --username=" + subversion_username \
                  + " " + subversion_url + repo_list[i] + \
                  " -T trunk -b branches -t tags"
        print(counter + command)
        # TODO: Handle perl.exe.stackdump child process exception.

        if os.system(command) == 0:
            print("[✓] " + subversion_url + repo_list[i] + " completed the migration process successfully.\n")
            correct_repo_list.append(subversion_url + repo_list[i])
        else:
            print("\n[x] " + subversion_url + repo_list[i] + " completed the migration process with error status.\n")
            incorrect_repo_list.append(subversion_url + repo_list[i])
    return correct_repo_list, incorrect_repo_list


def show_repo_migration_results(subversion_url, total_repos, correct_repo_list, incorrect_repo_list):
    print("[*] The migration process ended. "
          + str(total_repos) + " Were processed, "
          + str(len(correct_repo_list)) + " were correct, and "
          + str(len(incorrect_repo_list)) + " had errors.\n")

    print("[✓] Correct repositories: ")
    for correct_repo in correct_repo_list:
        print("[✓] " + subversion_url, correct_repo)

    print("\n[x] Incorrect repositories: ")
    for correct_repo in correct_repo_list:
        print("[x] " + subversion_url, correct_repo)
    # TODO: Save results to files.


def __main__():
    subversion_url, subversion_username, subversion_password = prompt_subversion_server_credentials()
    response = get_subversion_server_response(subversion_url, subversion_username, subversion_password)
    repo_list = parse_response_to_repo_list(response)
    correct_repo_list, incorrect_repo_list = migrate_repositories(subversion_url, subversion_username, repo_list)
    show_repo_migration_results(subversion_url, len(repo_list), correct_repo_list, incorrect_repo_list)


if __name__ == "__main__":
    __main__()
