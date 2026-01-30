import shutil
import textwrap
import platform
import os 
import re


PLATFORM: str = platform.system()
PWSH_PATH = shutil.which("powershell.exe")

# =============================================================================
# MAIN
# =============================================================================

def format_command(command, sep, format):
    if format:
        command = textwrap.dedent(command).strip()
        command = [c.strip() for c in command.splitlines() if not c.startswith("#") and c.strip()]
        command = sep.join(command)
    if PLATFORM != "Windows": # even thow we not want to format, we need to replace double quoutes with single
        command = command.replace('""', '"')
    print(f"\033[92mCommand: {command.replace("\n", " | ")}\033[0m")
    return command

def run(c, command, cmd = True, sep = " && ", format = True):
    if PLATFORM =="Windows":
        if cmd: # cmd
            command = format_command(command, sep, format)
            result = c.run(command, hide=True, warn=True)
        else: # pwsh
            command = format_command(command, sep, format)
            result = c.run(command, hide=True, warn=True, shell=PWSH_PATH) 
    else: # bash
        result = c.run(command, hide=True, warn=True)            
    exit, err, out = result.exited, result.stderr.strip(),result.stdout.strip()
    print(f"{'exit code: ': <10} {exit}")
    if err:
        print(f"{'stderr: ': <10}\n{err}")
    if out:
        print(f"{'stdout: ': <10}\n{out}")
    return result.exited

# =============================================================================
# FUNCTIONS
# =============================================================================

def get_next_version(c):
    # 1. Získáme tagy seřazené podle verze (nejnovější první)
    res = c.run("git tag --sort=-v:refname", hide=True, warn=True)
    tags = res.stdout.splitlines()
    
    version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"
    last_tag = None
    
    for tag in tags:
        if re.match(version_pattern, tag):
            last_tag = tag
            break

    # 2. Pokud není žádný tag, výchozí start je 0.1.0
    if not last_tag:
        return "0.1.0"

    # 3. Podíváme se na commity OD posledního tagu do teď
    log_res = c.run(f"git log {last_tag}..HEAD --format=%s", hide=True, warn=True)
    commits_since_tag = log_res.stdout.splitlines()

    # Pokud nejsou žádné nové commity, není co zvyšovat
    if not commits_since_tag:
        return None

    # 4. Hledáme "feat:" v nových commitech
    has_feat = any(commit.strip().startswith("feat:") for commit in commits_since_tag)

    if has_feat:
        major, minor, patch = map(int, last_tag.split('.'))
        minor += 1
        patch = 0
        return f"{major}.{minor}.{patch}"
    
    # Pokud jsou nové commity, ale žádný není "feat:", vracíme None
    return None

def update_pyproject_version(new_version):
    path = "pyproject.toml"
    if not os.path.exists(path):
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Hledá: version = "libovolná_stará_verze"
    # Nahradí: version = "new_version"
    new_content = re.sub(
        r'version\s*=\s*"\d+\.\d+\.\d+"', 
        f'version = "{new_version}"', 
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

# @task
# def bump(c):
#     new_ver = get_next_version(c)
    
#     print(f"{' VERSION CHECK ':=^50}") 
#     if new_ver:
#         print(f"Nová verze k vydání: {new_ver}")
#         update_pyproject_version(new_ver)
#         c.run("git add .")
#         c.run(f'git commit --allow-empty -m "{new_ver}"', hide=True)

#         # 3. Vytvoření tagu
#         print(f"Vytvářím tag {new_ver}...")
#         c.run(f'git tag -a {new_ver} -m "Version {new_ver}"')