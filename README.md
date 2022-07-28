# Svntogit: subversion to git migration tool

Svntogit is a script that allows for cloning of Subversion repositories and converting them to Git. 
It consults the index of repositories, lists them and then uses either `SubGit` or `git svn clone`  to convert them.

##  How it works
This script will download and convert all repositories from Subversion server from SVN to Git. In order to do that prompts for the needed credentials to access the server's repository list and catches it in HTML format. Using BeautifulSoup it filters the links for the repositories into a list.
Once this first stage is done, next is the migration itself of every repository. At the end, the migration results are shown and registered into correct and incorrect files lists.

## Using Svntogit as a Python script

### Before you begin, make sure you have these installed in your system:
 * [Python 3](https://www.python.org/downloads/) to run the script.
 * [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) library to filter server response to a repo list, to download it you can use `pip install bs4`.
 * [TMate SubGit](https://subgit.com/download) if you prefer to use the SubGit flavor of the script.
 * [Git](https://git-scm.com/downloads) to manage the cloned repositories.


### Now you can use the script directly from the terminal, to do so:
 * Copy the svntogit-subgit.py file into the folder you want all the new Git repositories to be stored.
 * Use `python3 svntogit-subgit.py` enter your credentials and wait all the repositories to be processed.
 
 ## Using Svntogit as an executable
> Comming soon

