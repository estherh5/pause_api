from contextlib import contextmanager
from datetime import datetime, timezone

from sqlalchemy import JSON, Integer, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


engine = None
Session = sessionmaker(expire_on_commit=False)


def configure_database(database_url):
    global engine

    if engine is not None:
        engine.dispose()

    # Heroku's Postgres add-on sets DATABASE_URL with the legacy "postgres://"
    # scheme, which SQLAlchemy no longer recognises. Normalise it to the
    # canonical "postgresql://" so the engine can load the dialect.
    if database_url.startswith("postgres://"):
        database_url = "postgresql://" + database_url[len("postgres://") :]

    engine_options = {}
    if not database_url.startswith("sqlite"):
        engine_options["pool_pre_ping"] = True

    engine = create_engine(database_url, **engine_options)
    Session.configure(bind=engine)
    return engine


@contextmanager
def session_scope():
    session = Session()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Activities(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    activities: Mapped[dict | str] = mapped_column(JSON, nullable=False)
    chart_types: Mapped[dict | str] = mapped_column(JSON, nullable=False)
    time_unit: Mapped[str] = mapped_column(Text, nullable=False)
    month: Mapped[str | None] = mapped_column(Text)
    year: Mapped[int | None] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )
