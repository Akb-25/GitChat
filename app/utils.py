import os
import re
import shutil
import stat
import subprocess

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def url_name(url: str) -> str:
    
    pattern = r"https?://github.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    if match:
        owner = match.group(1)
        repo = match.group(2)
        return f"{owner}_{repo}"
    else:
        raise ValueError("Invalid GitHub URL")

def clone_repo(git_url: str, repo_path: str):
    
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=on_rm_error)
    
    git_url = git_url.replace(".git", "")
    
    command = f'git clone {git_url}.git {repo_path}'
    subprocess.run(command, shell=True, check=True)

    git_dir = os.path.join(repo_path, '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, onerror=on_rm_error)

def model_prompt():
    
    system_prompt = """You are a helpful assistant with strong coding knowledge. Use the provided context to answer user questions with detailed explanations.
    Read the given context before answering, and think step-by-step. If you cannot answer based on the context, state that you don't have enough information. Do not use any external knowledge. Always mention the filename(s) from metadata in your answer."""
    instruction = "Context: {context}\nUser: {question}"
    
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<SYS>>\n", "\n<</SYS>>\n\n"
    
    SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    
    return prompt_template