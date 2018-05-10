import spectreapi
from spectreapi.zone import Zone
import pytest

@pytest.fixture()
def server():
    return spectreapi.UsernameServer('6hour','admin','admin')

