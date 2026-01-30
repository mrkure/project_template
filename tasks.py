from invoke import task # type: ignore
import os
from tasks_ import run

@task
def commit(c, message):
    run(c, """
        git --version
        git -c core.safecrlf=false add .
        """)
    run(c, f'git commit --allow-empty -m ""{message}""', cmd = False, format = False)

@task
def testpath(c):
    run(c, """
        if (Test-Path "pyproject.toml")
         { echo "Soubor nalezen!" }
         else 
        { echo "Chybi to!" }
        """, cmd = False, format = True, sep = "\n")






