
import os
from jinja2.ext import Extension
from pathlib import Path
import os

def user_name() -> str:
    return os.getlogin()

def project_namea() -> str:
    return "Path.cwd().name"

def slugify(value):
    return value.lower().replace(" ", "_").replace("-", "_")

class MyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["user_name"] = user_name
        environment.globals["user_name"] = project_namea

class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = slugify