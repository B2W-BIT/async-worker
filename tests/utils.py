import os

CURRENT_DIR = os.path.dirname(__file__)
FIXTURES_PATH = os.path.join(CURRENT_DIR, 'fixtures')


def get_fixture(file_name: str) -> str:
    with open(os.path.join(FIXTURES_PATH, file_name), encoding='utf-8') as fp:
        return fp.read()
