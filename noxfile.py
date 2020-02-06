import nox


@nox.session(python=["3.6", "3.7", "3.8"])
def tests(session):
    # args = session.posargs or ["--cov"]
    args = session.posargs
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


locations = "ccaaws", "noxfile.py", "tests"


@nox.session(python=["3.6", "3.7", "3.8"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-bugbear", "flake8-import-order")
    session.run("flake8", *args)
