import pytest

from pause import models
from server import create_app


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "pause-test.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": f"sqlite:///{database_path}",
        }
    )
    models.Base.metadata.create_all(models.engine)

    yield app

    models.Base.metadata.drop_all(models.engine)
    models.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()
