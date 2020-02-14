import tempfile

import nox

nox.options.sessions = "lint", "safety", "mypy"

locations = "ccaaws", "noxfile.py", "tests"


def install_with_constraints(session, *args, **kwargs):
    """Installs using pip's constraints.

    Args:
        session: the nox session
        args: the args
        kwargs: any kwargs
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.6", "3.7", "3.8"])
def tests(session):
    """Main pytest tests.

    Args:
        session: the nox session
    """
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov", "moto")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def xtest(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def lint(session):
    """Main linting session.

    Args:
        session: the nox session
    """
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def safety(session):
    """Check with safety plugin.

    Args:
        session: the nox session
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.8"])
def mypy(session):
    """Type checking with mypy.

    Args:
        session: the nox session
    """
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)
