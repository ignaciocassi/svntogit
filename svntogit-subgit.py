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


def migrate_repositories(repo_list, subversion_url, subversion_username, subversion_password):
    for repo in repo_list:
        # subgit configure http://sources.aa2000.com.ar/subversion/tca-fe-core/
        print("\n[*] subgit configure " + subversion_url + repo+"\n")
        os.system("subgit configure " + subversion_url + repo)
        # Agregar "username password" en el archivo tca-fe-core.git\subgit\passwd
        append_credentials_to_passwd_file(os.getcwd() + "\\" + repo.replace("/", "") + ".git" + "\\subgit\\passwd",
                                          subversion_username, subversion_password)
        # subgit install tca-fe-core.git
        print("\n[*]] subgit install " + repo.replace("/", "") + ".git\n")
        os.system("subgit install " + repo.replace("/", "") + ".git")
        # git clone tca-fe-core repos.git
        print("\n[*] git clone " + repo.replace("/", "") + " " + repo + ".git\n")
        os.system("git clone " + repo.replace("/", "") + " " + repo + ".git")


def append_credentials_to_passwd_file(passwd_file_path, subversion_username, subversion_password):
    try:
        # command = "ren "+passwd_file_path+" "+passwd_file_path+".txt"
        # os.system("ren "+passwd_file_path+" "+passwd_file_path+".txt")
        file = open(passwd_file_path, "wt")
        file.write(subversion_username + " " + subversion_password)
    except IOError:
        print("[*] passwd.txt file was not found.")
    finally:
        file.close()
        # os.system("ren " + passwd_file_path + ".txt " + passwd_file_path)


def __main__():
    subversion_url, subversion_username, subversion_password = prompt_subversion_server_credentials()
    response = get_subversion_server_response(subversion_url, subversion_username, subversion_password)
    repo_list = parse_response_to_repo_list(response)
    migrate_repositories(repo_list, subversion_url, subversion_username, subversion_password)


if __name__ == "__main__":
    __main__()
