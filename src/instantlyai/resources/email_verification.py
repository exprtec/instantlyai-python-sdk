"""Email verification resource: ``client.email_verification``."""

from __future__ import annotations

from .._transport import NOT_GIVEN, NotGiven
from ..models import EmailVerification as EmailVerificationModel
from ._base import AsyncAPIResource, SyncAPIResource

__all__ = ["AsyncEmailVerification", "EmailVerification"]


class EmailVerification(SyncAPIResource):
    def create(
        self, *, email: str, webhook_url: str | NotGiven = NOT_GIVEN
    ) -> EmailVerificationModel:
        """Create (kick off) an email verification."""
        return EmailVerificationModel.model_validate(
            self._post(
                "/api/v2/email-verification", json={"email": email, "webhook_url": webhook_url}
            )
        )

    def retrieve(self, email: str) -> EmailVerificationModel:
        """Check an email verification status."""
        return EmailVerificationModel.model_validate(
            self._get(f"/api/v2/email-verification/{email}")
        )


class AsyncEmailVerification(AsyncAPIResource):
    async def create(
        self, *, email: str, webhook_url: str | NotGiven = NOT_GIVEN
    ) -> EmailVerificationModel:
        """Create (kick off) an email verification."""
        return EmailVerificationModel.model_validate(
            await self._post(
                "/api/v2/email-verification", json={"email": email, "webhook_url": webhook_url}
            )
        )

    async def retrieve(self, email: str) -> EmailVerificationModel:
        """Check an email verification status."""
        return EmailVerificationModel.model_validate(
            await self._get(f"/api/v2/email-verification/{email}")
        )
