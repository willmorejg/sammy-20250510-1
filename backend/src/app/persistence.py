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

from abc import ABC, abstractmethod
from typing import Dict, Generic, List, TypeVar
from uuid import UUID

T = TypeVar("T")


class PersistenceProxy(ABC, Generic[T]):
    """Abstract base class defining the persistence interface."""

    @abstractmethod
    def create(self, obj: T) -> T:
        """Persist a new object."""

    @abstractmethod
    def read(self, obj_id: UUID) -> T:
        """Retrieve an object by its UUID."""

    @abstractmethod
    def update(self, obj_id: UUID, obj: T) -> T:
        """Update an existing object."""

    def upsert(self, obj: T) -> T:
        """Insert or update an object."""
        try:
            return self.update(obj.id, obj)
        except KeyError:
            return self.create(obj)

    @abstractmethod
    def delete(self, obj_id: UUID) -> None:
        """Delete an object by its UUID."""

    @abstractmethod
    def list_all(self) -> List[T]:
        """List all persisted objects."""


class InMemoryProxy(PersistenceProxy[T]):
    """In-memory implementation of the PersistenceProxy interface."""

    def __init__(self):
        self._storage: Dict[UUID, T] = {}

    def create(self, obj: T) -> T:
        self._storage[obj.id] = obj
        return obj

    def read(self, obj_id: UUID) -> T:
        return self._storage[obj_id]

    def update(self, obj_id: UUID, obj: T) -> T:
        self._storage[obj_id] = obj
        return obj

    def delete(self, obj_id: UUID) -> None:
        self._storage.pop(obj_id, None)

    def list_all(self) -> List[T]:
        return list(self._storage.values())
