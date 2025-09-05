import os
import pytest
from django.conf import settings


def test_timezone_setup():
    """Test czy strefa czasowa jest ustawiona."""
    print(f"TZ from env: {os.environ.get('TZ')}")
    print(f"Django TIME_ZONE: {settings.TIME_ZONE}")

    assert os.environ.get('TZ') == 'UTC'