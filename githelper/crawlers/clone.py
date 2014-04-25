import subprocess

def git(*args):
    return subprocess.check_call(['git'] + list(args))

# examples
git("status")
git("clone", "https://github.com/PredictionIO/PredictionIO.git")
