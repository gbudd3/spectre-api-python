import spectreapi
import pytest

@pytest.fixture()
def server():
    return spectreapi.UsernameServer('6hour','admin','admin')

