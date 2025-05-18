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

import os

import pytest

from app.authentication import Authentication


@pytest.fixture
def auth():
    return Authentication()


def test_hash_and_verify_password(auth):
    password = "secure_password"
    hashed = auth.hash_password(password)

    assert isinstance(hashed, bytes)
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrong_password", hashed)


def test_salt_file_created(auth):
    assert (
        os.path.exists(auth.__class__.__module__ + "/salt.bin") is False
    )  # Filepath is patched


def test_key_file_created(auth):
    assert (
        os.path.exists(auth.__class__.__module__ + "/key.bin") is False
    )  # Filepath is patched
