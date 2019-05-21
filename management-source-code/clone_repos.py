#!/usr/bin/env python3

import sys
import argparse
import getpass
import pathlib
from time import sleep

import requests
import subprocess
import logging

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)

parser = argparse.ArgumentParser()
parser.add_argument("DIR", type=str, const=True, nargs="?",
                    help="the directory to clone repos into")
parser.add_argument("URL", type=str, const=True, nargs="?",
                    help="the URL to the TFS repository, defaults to https://tfs-glo-lexisadvance.visualstudio.com",
                    default="https://tfs-glo-lexisadvance.visualstudio.com")
parser.add_argument("-u", "--user", type=str, dest="USER", const=True, required=True, nargs="?",
                    help="the user to be used to connect to TFS")
parser.add_argument("-p", "--pass", type=str, dest="PASS", const=True, nargs="?",
                    help="the password to be used to connect to TFS, if not present you will be prompted for this")
parser.add_argument("-s", "--ssh", dest="SSH", action='store_true',
                    help="Use SSH to clone [recommended]")


def main():
    args = parser.parse_args()
    repos_uri = "/_apis/git/repositories?api-version=1.0"

    if args.PASS is None:
        pw = getpass.getpass()
    else:
        pw = args.PASS

    response = requests.get(args.URL + repos_uri, auth=(args.USER, pw))
    response_json = None
    if response.status_code == 200:
        response_json = response.json()
    else:
        logging.error("There was a problem getting the repos from TFS, got {} {}".format(response.status_code, response.reason))
        if response.text is not None and response.text is not '':
            logging.error(response.text)
        exit(1)

    if response_json is not None:
        clone_repos(response_json['value'], args.DIR, args.SSH)


def clone_repos(repos, directory, use_ssh):
    for repo in repos:
        clone_path = pathlib.Path(f"{directory}/{repo['project']['name']}/{repo['name']}")

        if not clone_path.exists():
            clone_path.mkdir(parents=True)

            if use_ssh:
                clone_url = repo['sshUrl']
            else:
                clone_url = repo['remoteUrl']
                logging.warning("This does not manage answer prompts for password for you, if you want this, use SSH")
                sleep(5)

            logging.info(f"Cloning from {clone_url}")
            git("clone", clone_url, clone_path.absolute())
        else:
            # Presumably the repo has already been cloned so let's just fetch it again
            logging.info(f"Directory {clone_path.absolute()} already exists, attempting to fetch repository")
            git("-C", clone_path.absolute(), "fetch")


def git(*args):
    try:
        return subprocess.check_call(['git'] + list(args))
    except Exception as e:
        logging.error(f"Failed to execute [{args}], {str(e)}")


if __name__ == '__main__':
    main()
