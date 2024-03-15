import argparse
import subprocess


TEST_PATHS = [
    ("heathcheck", "server/services/heathcheck/tests"),
    ("core", "server/core/tests"),
    ("auth", "server/services/auth/tests"),
    ("recipe", "server/services/recipe/tests")
]


def get_services():
    parser = argparse.ArgumentParser(description="Process services.")
    parser.add_argument(
        "--service", nargs="+", help="List of services", required=False)
    return parser.parse_args().service


def test_cmd(path: str) -> list:
    return ["python", "-m", "pytest", path, "-W", "ignore::DeprecationWarning"]  # noqa


def run_pytest():
    services = get_services()

    paths = [
        path
        for service, path in TEST_PATHS
        if services is None or service in services
    ]
    for path in paths:
        cmd = test_cmd(path)
        subprocess.run(cmd)


if __name__ == "__main__":
    run_pytest()
