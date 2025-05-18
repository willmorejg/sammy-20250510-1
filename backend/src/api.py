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

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .app.services import (
    ComponentService,
    PasswordService,
    RoleAuthService,
    RoleService,
    SystemService,
    UserAuthService,
    UserService,
)
from .app.sqlmodel_models import (
    Component,
    Password,
    Role,
    RoleAuth,
    System,
    User,
    UserAuth,
)

app = FastAPI(title="SAMmy API", description="API for System and Component Management")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Origins allowed to access
    allow_credentials=True,           # Allows cookies, auth headers
    allow_methods=["*"],              # HTTP methods: GET, POST, etc.
    allow_headers=["*"],              # HTTP headers
)

# Service dependencies
def get_user_service():
    """Dependency to get the UserService instance"""
    return UserService()


def get_password_service():
    """Dependency to get the PasswordService instance"""
    return PasswordService()


def get_role_service():
    """Dependency to get the RoleService instance"""
    return RoleService()


def get_role_auth_service():
    """Dependency to get the RoleAuthService instance"""
    return RoleAuthService()


def get_user_auth_service():
    """Dependency to get the UserAuthService instance"""
    return UserAuthService()


def get_component_service():
    """Dependency to get the ComponentService instance"""
    return ComponentService()


def get_system_service():
    """Dependency to get the SystemService instance"""
    return SystemService()


# Create routers
user_router = APIRouter(prefix="/users", tags=["Users"])
password_router = APIRouter(prefix="/passwords", tags=["Passwords"])
role_router = APIRouter(prefix="/roles", tags=["Roles"])
role_auth_router = APIRouter(prefix="/role-auths", tags=["Role Authorizations"])
user_auth_router = APIRouter(prefix="/user-auths", tags=["User Authorizations"])
component_router = APIRouter(prefix="/components", tags=["Components"])
system_router = APIRouter(prefix="/systems", tags=["Systems"])


# User endpoints
@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    """Create a new user"""
    return service.create(user)


@user_router.get("/{user_id}", response_model=User)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Get a user by ID"""
    try:
        return service.read(user_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )


@user_router.get("/", response_model=List[User])
def list_users(service: UserService = Depends(get_user_service)):
    """List all users"""
    return service.list_all()


@user_router.put("/{user_id}", response_model=User)
def update_user(
    user_id: UUID, user: User, service: UserService = Depends(get_user_service)
):
    """Update a user by ID"""
    try:
        service.update(user_id, user)
        return service.read(user_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Delete a user by ID"""
    try:
        service.delete(user_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )


# Password endpoints
@password_router.post("/", response_model=Password, status_code=status.HTTP_201_CREATED)
def create_password(
    password: Password, service: PasswordService = Depends(get_password_service)
):
    """Create a new password"""
    return service.create(password)


@password_router.get("/{password_id}", response_model=Password)
def get_password(
    password_id: UUID, service: PasswordService = Depends(get_password_service)
):
    """Get a password by ID"""
    try:
        return service.read(password_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Password with ID {password_id} not found",
        )


@password_router.put("/{password_id}", response_model=Password)
def update_password(
    password_id: UUID,
    password: Password,
    service: PasswordService = Depends(get_password_service),
):
    """Update a password by ID"""
    try:
        service.update(password_id, password)
        return service.read(password_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Password with ID {password_id} not found",
        )


@password_router.delete("/{password_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_password(
    password_id: UUID, service: PasswordService = Depends(get_password_service)
):
    """Delete a password by ID"""
    try:
        service.delete(password_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Password with ID {password_id} not found",
        )


# Role endpoints
@role_router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_role(role: Role, service: RoleService = Depends(get_role_service)):
    """Create a new role"""
    return service.create(role)


@role_router.get("/{role_id}", response_model=Role)
def get_role(role_id: UUID, service: RoleService = Depends(get_role_service)):
    """Get a role by ID"""
    try:
        return service.read(role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found",
        )


@role_router.get("/", response_model=List[Role])
def list_roles(service: RoleService = Depends(get_role_service)):
    """List all roles"""
    return service.list_all()


@role_router.put("/{role_id}", response_model=Role)
def update_role(
    role_id: UUID, role: Role, service: RoleService = Depends(get_role_service)
):
    """Update a role by ID"""
    try:
        service.update(role_id, role)
        return service.read(role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found",
        )


@role_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: UUID, service: RoleService = Depends(get_role_service)):
    """Delete a role by ID"""
    try:
        service.delete(role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found",
        )


# RoleAuth endpoints
@role_auth_router.post(
    "/", response_model=RoleAuth, status_code=status.HTTP_201_CREATED
)
def create_role_auth(
    role_auth: RoleAuth, service: RoleAuthService = Depends(get_role_auth_service)
):
    """Create a new role authorization"""
    # Verify that the role exists before creating a role auth
    role_service = RoleService()
    try:
        role_service.read(role_auth.role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_auth.role_id} not found",
        )
    return service.create(role_auth)


@role_auth_router.get("/{role_auth_id}", response_model=RoleAuth)
def get_role_auth(
    role_auth_id: UUID, service: RoleAuthService = Depends(get_role_auth_service)
):
    """Get a role authorization by ID"""
    try:
        return service.read(role_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role authorization with ID {role_auth_id} not found",
        )


@role_auth_router.get("/", response_model=List[RoleAuth])
def list_role_auths(service: RoleAuthService = Depends(get_role_auth_service)):
    """List all role authorizations"""
    return service.list_all()


@role_auth_router.put("/{role_auth_id}", response_model=RoleAuth)
def update_role_auth(
    role_auth_id: UUID,
    role_auth: RoleAuth,
    service: RoleAuthService = Depends(get_role_auth_service),
):
    """Update a role authorization by ID"""
    try:
        # Verify that the role exists
        role_service = RoleService()
        try:
            role_service.read(role_auth.role_id)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {role_auth.role_id} not found",
            )
        service.update(role_auth_id, role_auth)
        return service.read(role_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role authorization with ID {role_auth_id} not found",
        )


@role_auth_router.delete("/{role_auth_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_auth(
    role_auth_id: UUID, service: RoleAuthService = Depends(get_role_auth_service)
):
    """Delete a role authorization by ID"""
    try:
        service.delete(role_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role authorization with ID {role_auth_id} not found",
        )


# UserAuth endpoints
@user_auth_router.post(
    "/", response_model=UserAuth, status_code=status.HTTP_201_CREATED
)
def create_user_auth(
    user_auth: UserAuth, service: UserAuthService = Depends(get_user_auth_service)
):
    """Create a new user authorization"""
    # Verify that user and role exist before creating
    user_service = UserService()
    role_service = RoleService()

    try:
        user_service.read(user_auth.user_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_auth.user_id} not found",
        )

    try:
        role_service.read(user_auth.role_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {user_auth.role_id} not found",
        )

    return service.create(user_auth)


@user_auth_router.get("/{user_auth_id}", response_model=UserAuth)
def get_user_auth(
    user_auth_id: UUID, service: UserAuthService = Depends(get_user_auth_service)
):
    """Get a user authorization by ID"""
    try:
        return service.read(user_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User authorization with ID {user_auth_id} not found",
        )


@user_auth_router.get("/", response_model=List[UserAuth])
def list_user_auths(service: UserAuthService = Depends(get_user_auth_service)):
    """List all user authorizations"""
    return service.list_all()


@user_auth_router.put("/{user_auth_id}", response_model=UserAuth)
def update_user_auth(
    user_auth_id: UUID,
    user_auth: UserAuth,
    service: UserAuthService = Depends(get_user_auth_service),
):
    """Update a user authorization by ID"""
    try:
        # Verify user and role exist
        user_service = UserService()
        role_service = RoleService()

        try:
            user_service.read(user_auth.user_id)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_auth.user_id} not found",
            )

        try:
            role_service.read(user_auth.role_id)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {user_auth.role_id} not found",
            )

        service.update(user_auth_id, user_auth)
        return service.read(user_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User authorization with ID {user_auth_id} not found",
        )


@user_auth_router.delete("/{user_auth_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_auth(
    user_auth_id: UUID, service: UserAuthService = Depends(get_user_auth_service)
):
    """Delete a user authorization by ID"""
    try:
        service.delete(user_auth_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User authorization with ID {user_auth_id} not found",
        )


# Component endpoints
@component_router.post(
    "/", response_model=Component, status_code=status.HTTP_201_CREATED
)
def create_component(
    component: Component, service: ComponentService = Depends(get_component_service)
):
    """Create a new component"""
    return service.create(component)


@component_router.get("/{component_id}", response_model=Component)
def get_component(
    component_id: UUID, service: ComponentService = Depends(get_component_service)
):
    """Get a component by ID"""
    try:
        return service.read(component_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component with ID {component_id} not found",
        )


@component_router.get("/", response_model=List[Component])
def list_components(service: ComponentService = Depends(get_component_service)):
    """List all components"""
    return service.list_all()


@component_router.put("/{component_id}", response_model=Component)
def update_component(
    component_id: UUID,
    component: Component,
    service: ComponentService = Depends(get_component_service),
):
    """Update a component by ID"""
    try:
        service.update(component_id, component)
        return service.read(component_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component with ID {component_id} not found",
        )


@component_router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(
    component_id: UUID, service: ComponentService = Depends(get_component_service)
):
    """Delete a component by ID"""
    try:
        service.delete(component_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Component with ID {component_id} not found",
        )


# System endpoints
@system_router.post("/", response_model=System, status_code=status.HTTP_201_CREATED)
def create_system(system: System, service: SystemService = Depends(get_system_service)):
    """Create a new system"""
    return service.create(system)


@system_router.get("/{system_id}", response_model=System)
def get_system(system_id: UUID, service: SystemService = Depends(get_system_service)):
    """Get a system by ID"""
    try:
        return service.read(system_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System with ID {system_id} not found",
        )


@system_router.get("/", response_model=List[System])
def list_systems(service: SystemService = Depends(get_system_service)):
    """List all systems"""
    return service.list_all()


@system_router.put("/{system_id}", response_model=System)
def update_system(
    system_id: UUID,
    system: System,
    service: SystemService = Depends(get_system_service),
):
    """Update a system by ID"""
    try:
        service.update(system_id, system)
        return service.read(system_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System with ID {system_id} not found",
        )


@system_router.delete("/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system(
    system_id: UUID, service: SystemService = Depends(get_system_service)
):
    """Delete a system by ID"""
    try:
        service.delete(system_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System with ID {system_id} not found",
        )


# Add relationship management endpoints for many-to-many relationships
@system_router.post(
    "/{system_id}/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT
)
def add_component_to_system(
    system_id: UUID,
    component_id: UUID,
    system_service: SystemService = Depends(get_system_service),
    component_service: ComponentService = Depends(get_component_service),
):
    """Add a component to a system"""
    try:
        # Verify both system and component exist
        system = system_service.read(system_id)
        component_service.read(component_id)

        # This requires custom business logic as many-to-many relationships
        # aren't directly supported by the current service layer
        # For now, we'll just acknowledge the endpoint
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@system_router.delete(
    "/{system_id}/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_component_from_system(
    system_id: UUID,
    component_id: UUID,
    system_service: SystemService = Depends(get_system_service),
    component_service: ComponentService = Depends(get_component_service),
):
    """Remove a component from a system"""
    try:
        # Verify both system and component exist
        system = system_service.read(system_id)
        component_service.read(component_id)

        # This requires custom business logic as many-to-many relationships
        # aren't directly supported by the current service layer
        # For now, we'll just acknowledge the endpoint
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Register all routers
app.include_router(user_router)
app.include_router(password_router)
app.include_router(role_router)
app.include_router(role_auth_router)
app.include_router(user_auth_router)
app.include_router(component_router)
app.include_router(system_router)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint"""
    return {"title": "SAMmy API", "version": "0.1.0"}
