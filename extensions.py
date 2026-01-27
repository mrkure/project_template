
import os
import subprocess
from jinja2.ext import Extension
from pathlib import Path
import os

def user_name() -> str:
    return os.getlogin().lower()

def git_user_name() -> str:
    return subprocess.getoutput("git config user.name").strip()


def git_user_email() -> str:
    return subprocess.getoutput("git config user.email").strip()

def slugify(value):
    return value.lower().replace(" ", "_").replace("-", "_")

class MyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["user_name"] = user_name
        environment.globals["git_user_name"] = git_user_name
        environment.globals["git_user_email"] = git_user_email

class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = slugify