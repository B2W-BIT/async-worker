import os

CURRENT_DIR = os.path.dirname(__file__)
FIXTURES_PATH = os.path.join(CURRENT_DIR, "fixtures")


def get_fixture(file_name: str) -> str:
    with open(os.path.join(FIXTURES_PATH, file_name), encoding="utf-8") as fp:
        return fp.read()


def typed_any(cls):
    class Any(cls):
        def __eq__(self, other):
            return isinstance(self, other.__class__)

    return Any()
