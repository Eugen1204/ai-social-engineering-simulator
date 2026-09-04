from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.exceptions import AlreadySentError, NotSentYetError, \
    AlreadyOpenedError, NotOpenedYetError, AlreadyClickedError


@dataclass
class CampaignEmployee:
    campaign_id: UUID
    employee_id: UUID
    _sent_at: datetime | None = field(default=None, init=False)
    _opened_at: None | datetime = field(default=None, init=False)
    _clicked_at: None | datetime = field(default=None, init=False)
    _submitted_credentials: list | None = field(default=None, init=False)
    _risk_score: int = field(default=0, init=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CampaignEmployee):
            return False
        return self.campaign_id == other.campaign_id and self.employee_id == other.employee_id

    def mark_send(self, send_at: datetime | None = None) -> None:
        if self._sent_at is not None:
            raise AlreadySentError("the letter has already been sent")
        self._sent_at = send_at if send_at is not None else datetime.now(UTC)

    def mark_opened(self) -> None:
        if self._sent_at is None:
            raise NotSentYetError("you cannot open a letter that has not yet been sent")
        if self._opened_at is not None:
            raise AlreadyOpenedError("the letter has already been opened")
        self._opened_at = datetime.now(UTC)

    def mark_clicked(self) -> None:
        if self._sent_at is None:
            raise NotSentYetError("you cannot open a letter that has not yet been sent")
        if self._opened_at is None:
            raise NotOpenedYetError("You cannot click on a link if the email has not been opened")
        if self._clicked_at is not None:
            raise AlreadyClickedError("the user has already clicked on the link")
        self._clicked_at = datetime.now(UTC)

    @property
    def sent_at(self) -> datetime | None:
        return self._sent_at
