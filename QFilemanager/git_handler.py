import os
import datetime as dt

class commitInfo:
        def __init__(self, checksum, commit_message, author, when, diff):
            self.checksum = checksum
            self.commit_message = commit_message
            self.author = author
            self.when = when
            self.diff = diff

        def to_str()
            result = ''
            result += self.checksum + '\n'
            result += self.commit_message + '\n'
            result += self.author + '\n'
            result += self.when + '\n'
            result += self.diff + '\n'

def git_status(dir_path):
    os.chdir(dir_path)
    result = os.popen('git status').read()
    print('result: ' + result)
    if result == '':
        return False
    return True


def git_init(dir_path):
    os.chdir(dir_path)
    result = os.popen('git init').read()
    if "fatal: " in result:
        return False
    return True


def git_add(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git add "' + file_name + '"').read()
    return True


def git_restore(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True


def git_restore_staged(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore --staged "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True


def git_untrack(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm --cached "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True


def git_rm(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True


def git_mv(dir_path, file_name, new_name):
    os.chdir(dir_path)
    result = os.popen('git mv "' + file_name + '" "' + new_name + '"').read()
    if "fatal: " in result:
        return False
    return True


def git_commit(dir_path, commit_msg):
    os.chdir(dir_path)
    result = os.popen('git commit -m "' + commit_msg + '"').read()
    if "fatal: " in result:
        return False
    return True


def get_status_list(dir_path):
    os.chdir(dir_path)

    status_list = {}

    result = os.popen('git status').read().split('\n')

    # for changes staged
    staged_index = -1
    if 'Changes to be committed:' in result:
        staged_index = result.index('Changes to be committed:')

    staged = {}
    staged['renamed'] = []
    staged['new'] = []
    staged['modified'] = []
    staged['deleted'] = []

    if not staged_index == -1:
        i = 2
        while '\t' in result[staged_index + i]:
            if 'renamed' in result[staged_index + i].split()[0]:
                staged['renamed'].append(
                    " ".join(result[staged_index + i].split()[3:]))
            if 'new' in result[staged_index + i].split()[0]:
                staged['new'].append(
                    " ".join(result[staged_index + i].split()[2:]))
            if 'modified' in result[staged_index + i].split()[0]:
                staged['modified'].append(
                    " ".join(result[staged_index + i].split()[1:]))
            if 'deleted' in result[staged_index + i].split()[0]:
                staged['deleted'].append(
                    " ".join(result[staged_index + i].split()[1:]))
            i = i + 1

    # for changes not staged
    not_staged_index = -1
    if 'Changes not staged for commit:' in result:
        not_staged_index = result.index('Changes not staged for commit:')

    not_staged = {}
    not_staged['renamed'] = []
    not_staged['new'] = []
    not_staged['modified'] = []
    not_staged['deleted'] = []

    if not not_staged_index == -1:
        i = 3
        while '\t' in result[not_staged_index + i]:
            if 'renamed' in result[not_staged_index + i].split()[0]:
                not_staged['renamed'].append(
                    " ".join(result[not_staged_index + i].split()[3:]))
            if 'new' in result[not_staged_index + i].split()[0]:
                not_staged['new'].append(
                    " ".join(result[not_staged_index + i].split()[2:]))
            if 'modified' in result[not_staged_index + i].split()[0]:
                not_staged['modified'].append(
                    " ".join(result[not_staged_index + i].split()[1:]))
            if 'deleted' in result[not_staged_index + i].split()[0]:
                not_staged['deleted'].append(
                    " ".join(result[not_staged_index + i].split()[1:]))
            i = i + 1

    # for untracked files
    untracked_index = -1
    if 'Untracked files:' in result:
        untracked_index = result.index('Untracked files:')

    untracked = []

    if not untracked_index == -1:
        i = 2
        while '\t' in result[untracked_index + i]:
            untracked.append(" ".join(result[untracked_index + i].split()[0:]))
            i = i + 1

    status_list['staged'] = staged
    status_list['not_staged'] = not_staged
    status_list['untracked'] = untracked

    return status_list


def git_create_branch(dir_path, branch_name):
    os.chdir(dir_path)
    result = os.popen('git branch ' + branch_name).read()


def git_delete_branch(dir_path, branch_name):
    os.chdir(dir_path)
    result = os.popen('git branch -d ' + branch_name).read()


def git_show_branch_list(dir_path):
    os.chdir(dir_path)
    result = os.popen('git branch').read()
    branch_list = result.strip().split('\n')
    current_branch = 'main'
    for i in branch_list:
        if '*' in i:
            i = i[2:]
            current_branch = i
            print('Current branch : ' + current_branch + '\n')

    print(branch_list)
    return branch_list, current_branch


def git_rename_branch(dir_path, branch_name):
    os.chdir(dir_path)
    result = os.popen('git branch -m ' + branch_name).read()
    if "fatal: " in result:
        return False
    return True


def git_checkout_branch(dir_path, branch_name):
    os.chdir(dir_path)
    result = os.popen('git checkout ' + branch_name).read()
    print(branch_name+"으로 체크아웃 되었습니다")
    print(result)
    if "Already on " in result:
        return False
    return True


def git_merge(dir_path, to_be_merged):
    os.chdir(dir_path)
    # print("Branch name " + to_be_merged + "\n")
    result = os.popen('git merge ' + to_be_merged).read()
    # print("Git Merge : " + result + "\n")
    if "CONFLICT (content): " in result:
        result = result.split('\n')
        os.popen('git merge --abort')
        return result
    return True


def git_parse_log(dir_path):
    
    os.chdir(dir_path)
    result_graph = os.popen('git log --oneline --graph').read()
    result_log = os.popen('git log').read()
    result = result.strip().split('\n')

    graph_symbol = ['*', '|', '/', '\\', ' ']
    graph_data = []

    for result_graph_line in result_graph:
        # print('line :', result_line)
        graph_line = []
        for result_symbol in result_graph_line:
            if result_symbol in graph_symbol:
                graph_line.append(result_symbol)
            else:
                break
        # print(graph_line)
        graph_data.append(graph_line)

    log_data = []
    
    for result_log_idx in range(0, result_log):
        if 'commit' == result_log[result_log_idx].split()[0]:
            commit_info = ''
            num_parse_line = 5
            if 'Merge:' == result_log[result_log_idx + 1].split()[0]:
                num_parse_line = 6
            
            for parse_line in range(0, num_parse_line):
                commit_info += result_log[parse_line] + '\n'
            
            log_data.append(commit_info)

    return graph_data, log_data


def git_clone(dir_path, branch_name, id, token, url):
    from git import Repo

    os.chdir(dir_path)

    username = f"{id}"
    password = f"{token}"
    repo_name = url.split("//")[-1]
    repo_name_final = repo_name.split('/')[-1]
    repo_name_final = repo_name_final.split('.')[0]
    remote = f"https://{username}:{password}@{repo_name}"
    print("remote : " + remote)


    # git clone https://username@github.com/username/repo_name
    #os.popen('git clone '+'https://' + id +
    #         '@' + repo_name)
    tmp = os.popen('git ls-remote '+ remote).read()
    if '' == tmp:
        return False
    else:
        Repo.clone_from(remote, dir_path + '/' + repo_name_final)
        return True
