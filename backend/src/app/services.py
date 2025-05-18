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

from typing import Generic, TypeVar
from uuid import UUID

from .duckdb_persistence_proxy import DuckDBProxy
from .sqlmodel_models import Role  # updated import
from .sqlmodel_models import (
    Component,
    Password,
    RoleAuth,
    SQLModel,
    System,
    User,
    UserAuth,
)

# from app.models import Component, Password, Role, RoleAuth, System, User


T = TypeVar("T", bound=SQLModel)

# PROXY = InMemoryProxy[T]()


class CRUDService(Generic[T]):
    """CRUD service for managing objects of type T."""

    def __init__(self, model_cls: type[T]):  # , proxy: PersistenceProxy[T] = PROXY):
        self.proxy = DuckDBProxy(model_cls)  # Use DuckDBProxy for persistence

    def create(self, obj: T) -> T:
        """Create a new object."""
        return self.proxy.create(obj)

    def read(self, obj_id: UUID) -> T:
        """Read an object by its ID."""
        return self.proxy.read(obj_id)

    def update(self, obj_id: UUID, obj: T) -> T:
        """Update an existing object."""
        return self.proxy.update(obj_id, obj)

    def upsert(self, obj: T) -> T:
        """Update an existing object."""
        return self.proxy.upsert(obj)

    def delete(self, obj_id: UUID) -> None:
        """Delete an object by its ID."""
        self.proxy.delete(obj_id)

    def list_all(self):
        """List all objects."""
        return self.proxy.list_all()


class UserService(CRUDService[User]):
    """User service for managing user objects."""

    def __init__(self):
        super().__init__(User)


class PasswordService(CRUDService[Password]):
    """Password service for managing password objects."""

    def __init__(self):
        super().__init__(Password)


class RoleService(CRUDService[Role]):
    """Role service for managing role objects."""

    def __init__(self):
        super().__init__(Role)


class RoleAuthService(CRUDService[RoleAuth]):
    """Role authorization service for managing role authorization objects."""

    def __init__(self):
        super().__init__(RoleAuth)


class UserAuthService(CRUDService[UserAuth]):
    """User authorization service for managing user authorization objects."""

    def __init__(self):
        super().__init__(UserAuth)


class ComponentService(CRUDService[Component]):
    """Component service for managing component objects."""

    def __init__(self):
        super().__init__(Component)


class SystemService(CRUDService[System]):
    """System service for managing system objects."""

    def __init__(self):
        super().__init__(System)
