''' A module for evaluating the performance of git with
    dozens of branches
'''
import os
import subprocess
from itertools import product
import time
import string

def init_server_repo(path):
    ''' Initializes a Git-Server
    '''
    os.umask(0)
    try:
        os.mkdir(path, mode=0o777)
    except FileExistsError:
        print('[ERROR] Directory already exists')
    os.chdir(path)
    subprocess.run(["git", "init", "--bare"])
    os.chdir("..")

def init_client_repo(path, name=None):
    ''' Clones the repo
    path: remote repository location
    name: name of the cloned folder
    '''
    if name != None:
        subprocess.run(["git", "clone", path, name])
        return
    subprocess.run(["git", "clone", path])

def move_to_folder(path):
    ''' Changes the working directory
    '''
    os.chdir(path)

def init_credentials():
    ''' Initializes mail and password
    '''
    subprocess.run(["git", "config", "user.email", "test@example.com"])
    subprocess.run(["git", "config", "user.name", "Max Mustermann"])

def create_branch(name):
    ''' Create a new branch
    name: the name of the branch
    '''
    subprocess.run(["git", "checkout", "-b", name])

def create_file(filename):
    ''' Creates a sample file
    filename: The name of the file
    '''
    filepath = "./"+filename
    subprocess.run(["touch", filepath])

def add_file():
    ''' Stages all files
    '''
    subprocess.run(["git", "add", "."])

def set_push_origin(branchname):
    ''' Commits the current changes
    '''
    subprocess.run(["git", "push", "--set-upstream", "origin", branchname])

def edit_file(filename, text):
    ''' Appends to the sample file
    filename: The name of the file
    text: string to write to file
    '''
    filepath = "./"+filename
    cmd = f'echo "{text}" >> {filepath}'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def commit_changes():
    ''' Commits the current changes
    '''
    subprocess.run(["git", "commit", "-m", "'hello eugen'"])

def push_changes():
    ''' Pushes the changes to the repo
    '''
    subprocess.run(["git", "push"])

def checkout_master():
    ''' Checks out to master branch
    '''
    subprocess.run(["git", "checkout", "master"])

if __name__ == "__main__":
    REPO_PATH = "perf.git"
    FILE_NAME = "test"
    BRANCH_COUNT = 1_000_000

    branch_name = product(string.ascii_letters, repeat=10)

    # Initialize
    init_server_repo(REPO_PATH) # touch file an commit
    init_client_repo(REPO_PATH)
    move_to_folder("./perf")
    init_credentials()
    edit_file("./test", "master")
    add_file()
    commit_changes()
    push_changes()

    # # Create Branches
    starttime1 = time.time()
    for i in range(0, BRANCH_COUNT):
        BRANCH_NAME = ''.join(next(branch_name))
        create_branch(BRANCH_NAME)
        create_file(FILE_NAME)
        add_file()
        commit_changes()
        edit_file(FILE_NAME, BRANCH_NAME)
        add_file()
        commit_changes()
        set_push_origin(BRANCH_NAME)
        checkout_master()
    endtime1 = time.time()

    move_to_folder("../")

    starttime2 = time.time()
    init_client_repo(REPO_PATH, name="clone-test")
    endtime2 = time.time()

    print(f'[INFO] Created {BRANCH_COUNT/(endtime1-starttime1):.2f}branches/s')
    print(f'[INFO] Cloning the repo took {endtime2-starttime2:.2f}s')
