"""API integration tests for authentication and user endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestRegister:
    """POST /api/v1/auth/register"""

    def test_register_success(self, client: TestClient) -> None:
        payload = {
            "full_name": "New User",
            "email": "new@example.com",
            "password": "StrongPass1",
        }
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user"]["email"] == "new@example.com"
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_register_duplicate(self, client: TestClient, test_user) -> None:
        payload = {
            "full_name": "Duplicate",
            "email": test_user.email,
            "password": "StrongPass1",
        }
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 409

    def test_register_missing_field(self, client: TestClient) -> None:
        payload = {"email": "missing@example.com"}
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_weak_password(self, client: TestClient) -> None:
        payload = {
            "full_name": "Weak",
            "email": "weak@example.com",
            "password": "short",
        }
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 422


class TestLogin:
    """POST /api/v1/auth/login"""

    def test_login_success(self, client: TestClient, test_user) -> None:
        payload = {"email": test_user.email, "password": "TestPass123"}
        response = client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user"]["email"] == test_user.email
        assert "access_token" in data["data"]

    def test_login_wrong_password(self, client: TestClient, test_user) -> None:
        payload = {"email": test_user.email, "password": "WrongPass1"}
        response = client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 401

    def test_login_wrong_email(self, client: TestClient) -> None:
        payload = {"email": "unknown@example.com", "password": "SomePass1"}
        response = client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 401


class TestRefresh:
    """POST /api/v1/auth/refresh"""

    def test_refresh_success(self, client: TestClient, test_user) -> None:
        from app.core.security import create_refresh_token

        refresh = create_refresh_token(
            user_id=test_user.id,
            email=test_user.email,
            role=test_user.role,
        )
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]


class TestLogout:
    """POST /api/v1/auth/logout"""

    def test_logout(self, client: TestClient) -> None:
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"


class TestGetMe:
    """GET /api/v1/me"""

    def test_get_me_success(self, client: TestClient, auth_headers: dict) -> None:
        response = client.get("/api/v1/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] is not None

    def test_get_me_no_token(self, client: TestClient) -> None:
        response = client.get("/api/v1/me")
        assert response.status_code == 401


class TestUpdateMe:
    """PUT /api/v1/me"""

    def test_update_me_success(self, client: TestClient, auth_headers: dict) -> None:
        payload = {"full_name": "Updated Name"}
        response = client.put("/api/v1/me", json=payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"]["full_name"] == "Updated Name"


class TestChangePassword:
    """PUT /api/v1/me/password"""

    def test_change_password_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_user,
    ) -> None:
        payload = {
            "current_password": "TestPass123",
            "new_password": "NewPass1234",
        }
        response = client.put(
            "/api/v1/me/password",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 200

    def test_change_password_wrong_current(
        self,
        client: TestClient,
        auth_headers: dict,
    ) -> None:
        payload = {
            "current_password": "WrongPass1",
            "new_password": "NewPass1234",
        }
        response = client.put(
            "/api/v1/me/password",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 422


class TestAdminUsers:
    """GET /api/v1/users"""

    def test_list_users_as_admin(self, client: TestClient, admin_headers: dict) -> None:
        response = client.get("/api/v1/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_list_users_as_regular_user(
        self,
        client: TestClient,
        auth_headers: dict,
    ) -> None:
        response = client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == 401

    def test_get_user_as_admin(
        self,
        client: TestClient,
        admin_headers: dict,
        test_user,
    ) -> None:
        response = client.get(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers,
        )
        assert response.status_code == 200

    def test_update_user_role_as_admin(
        self,
        client: TestClient,
        admin_headers: dict,
        test_user,
    ) -> None:
        payload = {"role": "admin"}
        response = client.patch(
            f"/api/v1/users/{test_user.id}/role",
            json=payload,
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["data"]["role"] == "admin"
