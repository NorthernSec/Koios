import os

runpath = os.path.dirname(os.path.realpath(__file__))

def get_projects():
    projects = []
    for path, folders, files in os.walk(os.path.join(runpath, "..")):
        if "models.py" in files:
            projects.append(os.path.basename(path))
    return projects
