import urllib
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def prompt_subversion_server_credentials():
    subversion_url = input("[*] Please enter the URL address for target Subversion server: ")
    subversion_username = input("[*] Please enter the username for authenticating in Subversion server: ")
    subversion_password = input("[*] Please enter the password authenticating in Subversion server: ")
    return subversion_url, subversion_username, subversion_password


def get_subversion_server_response(subversion_url, subversion_username, subversion_password):
    url_opener, svn_request = get_url_opener_and_request(subversion_url, subversion_username, subversion_password)
    try:
        result = url_opener.open(svn_request)
        response = result.read()
        return response
    except HTTPError:
        print("[X] The username, password or URL entered are incorrect please try again...\n")
        prompt_subversion_server_credentials()


def get_url_opener_and_request(subversion_url, subversion_username, subversion_password):
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, subversion_url, subversion_username, subversion_password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    url_opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(url_opener)
    svn_request = urllib.request.Request(subversion_url)
    return url_opener, svn_request


def parse_response_to_repo_list(response):
    soup = BeautifulSoup(response, features="html.parser")
    return soup.find('ul')


def __main__():
    # TODO: Read and validate Subversion URL from user input.
    # TODO: Handle wrong credentials exception.
    # TODO: Implement html response processing to obtain the list of repository names.
    subversion_url, subversion_username, subversion_password = prompt_subversion_server_credentials()
    response = get_subversion_server_response(subversion_url, subversion_username, subversion_password)
    repo_list = parse_response_to_repo_list(response)


if __name__ == "__main__":
    __main__()
