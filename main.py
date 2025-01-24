from pathlib import Path
import filecmp
import json

APP_NAME                 = 'c-repo-organizer'
SCRIPT_DIR_PATH          = Path(__file__).parent.resolve()
GIT_DIR_PATH             = SCRIPT_DIR_PATH.parent
REPOS_LIST_FILE_PATH     = SCRIPT_DIR_PATH/'c_repos.json'
SAMPLE_DIR_NAME          = 'c-repo-sample'
SAMPLE_DIR_RELATIVE_PATH = Path(SAMPLE_DIR_NAME)

ANSI_ESC = '\033'
ANSI_PARAM_BEGIN = '['
ANSI_PARAM_END = 'm'
COLOR_PREFIX = ANSI_ESC + ANSI_PARAM_BEGIN
COLOR_SUFFIX = ANSI_PARAM_END
COLOR_RESET = COLOR_PREFIX + '0' + COLOR_SUFFIX
COLOR_RED = COLOR_PREFIX + '31' + COLOR_SUFFIX
COLOR_YELLOW = COLOR_PREFIX + '33' + COLOR_SUFFIX
COLOR_GREEN = COLOR_PREFIX + '32' + COLOR_SUFFIX

def colored_print(*args, color=COLOR_RESET, **kwargs):
    text = ' '.join(map(str, args))  # Mimic the way `print` joins arguments
    print(f'{color}{text}{COLOR_RESET}', flush=True, **kwargs)

def check_file(repo_path, file):
    colored_print(f'Checking {file}')
    if (repo_path/file).exists():
        if filecmp.cmp(SAMPLE_DIR_RELATIVE_PATH/file, repo_path/file, shallow=False):
            colored_print(f'File is identical', color=COLOR_GREEN)
            return True
        else:
            colored_print(f'File is not identical', color=COLOR_YELLOW)
            return False
    else:
        colored_print(f'File is missing', color=COLOR_RED)
        return False

def run_check():
    total_result = True
    files = [f.relative_to(SAMPLE_DIR_RELATIVE_PATH) for f in SAMPLE_DIR_RELATIVE_PATH.rglob('*') if (f.is_file() and (f.name != '.DS_Store'))]

    with open(REPOS_LIST_FILE_PATH, 'r') as f:
        json_repos_list = json.load(f)

    for repo in json_repos_list:
        colored_print(f'Checking repository: {repo}')
        repo_path = GIT_DIR_PATH/repo

        for file in files:
            total_result = total_result & check_file(repo_path, file)
        colored_print(f'Done repository: {repo}\n')
    return total_result

if __name__ == '__main__':
    colored_print(f'--- {APP_NAME} start ---')
    total_result = run_check()
    colored_print(f'\n{total_result=}', color=(COLOR_GREEN if total_result else COLOR_RED))
    colored_print(f'---  {APP_NAME} End  ---')
