from invoke import task # type: ignore
import os
from tasks_ import run

@task
def commit(c, message):
    run(c, """
        # git --version
        git -c core.safecrlf=false add .
        """)
    run(c, f'git commit --allow-empty -m ""{message}""', cmd = False, format = False)
    run(c, 'git push', cmd = False, format = False)

@task
def version(c):
    ex, err, out = run(c, 'semantic-release version --no-vcs-release --skip-build', cmd = True, format = False)
    run(c, 'git pull', cmd = True, format = False)    


@task
def versionb(c):
    ex, err, out = run(c, 'semantic-release version --no-vcs-release --skip-build', cmd = True, format = False)
    run(c, 'git pull', cmd = True, format = False)    
    if err.startswith("No release will be made"):
            run(c, 'echo uv build skipped', cmd = True, format = False)
    else:
        run(c, 'uv build', cmd = True, format = False)

@task
def testpath(c):
    run(c, """
        if (Test-Path "pyproject.toml")
         { echo "Soubor nalezen!" }
         else 
        { echo "Chybi to!" }
        """, cmd = False, format = True, sep = "\n")






