import pytest
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ':memory:',
        }
    },
    INSTALLED_APPS=[
        "user",
        "publication",
    ],
)


@pytest.mark.django_db
def pytest_configure():
    from django.db import connections
    connections["default"].ensure_connection()
