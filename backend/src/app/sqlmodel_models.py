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

# sqlmodel_models.py
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from .model_enum import ComponentType


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str
    auths: List["UserAuth"] = Relationship(back_populates="user")


class Password(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str


class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    role_auths: List["RoleAuth"] = Relationship(back_populates="role")
    user_auths: List["UserAuth"] = Relationship(back_populates="role")


class RoleAuth(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    feature_name: str
    role_id: uuid.UUID = Field(foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="role_auths")


class UserAuth(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    user: Optional[User] = Relationship(back_populates="auths")
    role: Optional[Role] = Relationship(back_populates="user_auths")


class SystemComponentLink(SQLModel, table=True):
    system_id: uuid.UUID = Field(foreign_key="system.id", primary_key=True)
    component_id: uuid.UUID = Field(foreign_key="component.id", primary_key=True)


class Component(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    type: ComponentType
    properties: List[Dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    systems: List["System"] = Relationship(
        back_populates="components", link_model=SystemComponentLink
    )


class System(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    components: List[Component] = Relationship(
        back_populates="systems", link_model=SystemComponentLink
    )
