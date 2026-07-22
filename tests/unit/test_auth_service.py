"""Unit tests for the Authentication service."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.exceptions.handlers import ConflictError, UnauthorizedError, ValidationError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import ChangePasswordRequest, UserUpdateRequest
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class TestAuthServiceRegister:
    """Tests for AuthService.register()."""

    def test_register_success(self, db_session: Session) -> None:
        service = AuthService(db_session)
        request = RegisterRequest(
            full_name="New User",
            email="new@example.com",
            password="StrongPass1",
        )
        result = service.register(request)

        assert "user" in result
        assert result["user"]["email"] == "new@example.com"
        assert result["user"]["role"] == "user"
        assert "access_token" in result
        assert "refresh_token" in result

    def test_register_duplicate_email(self, db_session: Session, test_user) -> None:
        service = AuthService(db_session)
        request = RegisterRequest(
            full_name="Duplicate",
            email=test_user.email,
            password="StrongPass1",
        )
        with pytest.raises(ConflictError):
            service.register(request)


class TestAuthServiceLogin:
    """Tests for AuthService.login()."""

    def test_login_success(self, db_session: Session, test_user) -> None:
        service = AuthService(db_session)
        request = LoginRequest(email=test_user.email, password="TestPass123")
        result = service.login(request)

        assert result["user"]["email"] == test_user.email
        assert "access_token" in result
        assert "refresh_token" in result

    def test_login_invalid_password(self, db_session: Session, test_user) -> None:
        service = AuthService(db_session)
        request = LoginRequest(email=test_user.email, password="WrongPass1")
        with pytest.raises(UnauthorizedError):
            service.login(request)

    def test_login_invalid_email(self, db_session: Session) -> None:
        service = AuthService(db_session)
        request = LoginRequest(email="unknown@example.com", password="SomePass1")
        with pytest.raises(UnauthorizedError):
            service.login(request)


class TestAuthServiceRefresh:
    """Tests for AuthService.refresh_token()."""

    def test_refresh_success(self, db_session: Session, test_user, user_token) -> None:
        from app.core.security import create_refresh_token

        service = AuthService(db_session)
        refresh = create_refresh_token(
            user_id=test_user.id,
            email=test_user.email,
            role=test_user.role,
        )
        from app.schemas.auth import RefreshRequest

        result = service.refresh_token(RefreshRequest(refresh_token=refresh))
        assert "access_token" in result


class TestUserService:
    """Tests for UserService."""

    def test_get_profile(self, db_session: Session, test_user) -> None:
        service = UserService(db_session)
        profile = service.get_profile(test_user.id)
        assert profile["email"] == test_user.email

    def test_update_profile(self, db_session: Session, test_user) -> None:
        service = UserService(db_session)
        request = UserUpdateRequest(full_name="Updated Name")
        profile = service.update_profile(test_user.id, request)
        assert profile["full_name"] == "Updated Name"

    def test_change_password_success(self, db_session: Session, test_user) -> None:
        service = UserService(db_session)
        request = ChangePasswordRequest(
            current_password="TestPass123",
            new_password="NewPass1234",
        )
        service.change_password(test_user.id, request)

        from app.core.security import verify_password
        from app.repositories.user_repository import UserRepository

        repo = UserRepository(db_session)
        user = repo.get_by_id(test_user.id)
        assert verify_password("NewPass1234", user.password_hash)

    def test_change_password_wrong_current(self, db_session: Session, test_user) -> None:
        service = UserService(db_session)
        request = ChangePasswordRequest(
            current_password="WrongPass1",
            new_password="NewPass1234",
        )
        with pytest.raises(ValidationError):
            service.change_password(test_user.id, request)
