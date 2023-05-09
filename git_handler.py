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

def get_status_list(dir_path):
    os.chdir(dir_path)

    status_list = {}

    result = os.popen('git status').read().split('\n')
    staged_index = result.find('changes to be committed:')
    
    staged = {}
    staged['new'] = []
    staged['modified'] = []
    staged['deleted'] = []

    if staged_index not -1:
        i = 2
        while '\tnew file' in result[staged_index + i]:
            staged['new'].append(result[staged_index + i])
            i = i + 1

        while '\tmodified' in result[staged_index + i]:
            staged['modified'].append(result[staged_index + i])
            i = i + 1

        while '\tdeleted' in result[staged_index + i]:
            staged['deleted'].append(result[staged_index + i])
            i = i + 1

    modified_index = result.index('changes not staged for commit:')

    untacked_index = result.index('Untracked_files:')

    return status_list
