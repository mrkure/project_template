
import os
from jinja2.ext import Extension


def user_name() -> str:
    return os.getlogin()

def slugify(value):
    return value.lower().replace(" ", "_").replace("-", "_")

class MyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["user_name"] = user_name


class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = slugify