import os

def git_status(dir_path):
    os.chdir(dir_path)
    result = os.popen('git status').read()
    return result

def git_init(dir_path):
    os.chdir(dir_path)
    result = os.popen('git init').read()
    return result

def git_add(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git add ' + file_name).read()
    return result

def git_restore(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore ' + file_name).read()
    return result

def git_restore_staged(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore --staged ' + file_name).read()
    return result

def git_untrack(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm --cached ' + file_name).read()
    return result

def git_rm(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm ' + file_name).read()
    return result

def git_mv(dir_path, file_name, new_name):
    os.chdir(dir_path)
    result = os.popen('git mv ' + file_name + ' ' + new_name).read()
    return result

def git_commit(dir_path, commit_msg):
    os.chdir(dir_path)
    result = os.popen('git commit -m "' + commit_msg + '"').read()
    return result
