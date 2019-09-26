#!usr/bin/python
""" This is a script for executing command via python and handling output. """
import subprocess

# A list of the changes
CHANGES = []


def bandit():
    """ Bandit controller function """
    print("Bandit!")


def git_changes():
    """ Are there changes to commit """
    changes = ["new file:", "modified:"]
    git_out = subprocess.Popen(['git', 'status'],
                               stdout=subprocess.PIPE)
    stdout = git_out.communicate()
    print(stdout)
    if any(condition in stdout for condition in changes):
        print("Okay")


def main():
    """ The main controller function """
    git_changes()
    if len(CHANGES) > 0:
        bandit()
    else:
        print("Nothing to Commit, Bro!")


if __name__ == '__main__':
    main()
