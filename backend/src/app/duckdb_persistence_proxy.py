# Copyright 2025 James G Willmore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# duckdb_proxy.py
import os
from typing import Generic, List, Type, TypeVar
from uuid import UUID

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .persistence import PersistenceProxy  # replace with actual import path
from .sqlmodel_models import SQLModel  # updated import

T = TypeVar("T", bound=SQLModel)

DEFAULT_DUCKDB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "resources",
    "example.duckdb",
)


class DuckDBProxy(PersistenceProxy[T], Generic[T]):
    """DuckDB-backed persistence proxy using SQLModel."""

    def __init__(self, model_cls: Type[T], db_path: str = DEFAULT_DUCKDB_PATH):
        """Initialize the DuckDB proxy.
        Args:
            model_cls (Type[T]): The SQLModel class to use for persistence.
            db_path (str): Path to the DuckDB database file.
        """
        self._model_cls = model_cls
        self._db_path = db_path
        self._create_tables()

    def _create_engine(self):
        """Create a SQLAlchemy engine and sessionmaker for DuckDB."""
        engine = create_engine(f"duckdb:///{self._db_path}")
        return engine, sessionmaker(bind=engine)

    def _create_tables(self):
        """Create tables in the DuckDB database if they do not exist."""
        engine, _ = self._create_engine()
        SQLModel.metadata.create_all(engine)
        engine.dispose()

    def create(self, obj: T) -> T:
        """Create a new object in the DuckDB database.
        Args:
            obj (T): The object to create.
        Returns:
            T: The created object with its ID populated.
        """
        engine, Session = self._create_engine()
        with Session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        engine.dispose()
        return obj

    def read(self, obj_id: UUID) -> T:
        """Read an object from the DuckDB database by its ID.
        Args:
            obj_id (UUID): The ID of the object to read.
        Returns:
            T: The object with the specified ID.
        Raises:
            KeyError: If the object with the specified ID does not exist.
        """
        engine, Session = self._create_engine()
        with Session() as session:
            result = session.get(self._model_cls, obj_id)
            if not result:
                raise KeyError(f"Object with ID {obj_id} not found")
        engine.dispose()
        return result

    def update(self, obj_id: UUID, obj: T) -> T:
        """Update an existing object in the DuckDB database.
        Args:
            obj_id (UUID): The ID of the object to update.
            obj (T): The updated object.
        Returns:
            T: The updated object.
        Raises:
            KeyError: If the object with the specified ID does not exist.
        """
        engine, Session = self._create_engine()
        with Session() as session:
            existing = session.get(self._model_cls, obj_id)
            if not existing:
                raise KeyError(f"Object with ID {obj_id} not found")
            for key, value in vars(obj).items():
                if key != "_sa_instance_state":
                    setattr(existing, key, value)
            session.commit()
        engine.dispose()
        return existing

    def delete(self, obj_id: UUID) -> None:
        """Delete an object from the DuckDB database by its ID.
        Args:
            obj_id (UUID): The ID of the object to delete.
        Raises:
            KeyError: If the object with the specified ID does not exist.
        """
        engine, Session = self._create_engine()
        with Session() as session:
            obj = session.get(self._model_cls, obj_id)
            if obj:
                session.delete(obj)
                session.commit()
        engine.dispose()

    def list_all(self) -> List[T]:
        """List all objects in the DuckDB database.
        Returns:
            List[T]: A list of all objects in the database.
        """
        engine, Session = self._create_engine()
        with Session() as session:
            results = session.scalars(select(self._model_cls)).all()
        engine.dispose()
        return results


# Example usage:
# from .sqlmodel_models import User
# proxy = DuckDBProxy(User)
# all_users = proxy.list_all()
