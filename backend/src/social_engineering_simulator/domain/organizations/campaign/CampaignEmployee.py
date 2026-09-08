from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID

from social_engineering_simulator.domain.organizations.campaign.exceptions import AlreadySentError, NotSentYetError, \
    AlreadyOpenedError, NotOpenedYetError


@dataclass
class CampaignEmployee:
    campaign_id: UUID
    employee_id: UUID
    _sent_at: datetime | None = field(default=None, init=False)
    _opened_at: None | datetime = field(default=None, init=False)
    _clicked_at: list[datetime] = field(default_factory=list, init=False)
    _submitted_credentials_at: list[datetime] = field(default_factory=list, init=False)
    _risk_score: float = field(default=0, init=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CampaignEmployee):
            return False
        return self.campaign_id == other.campaign_id and self.employee_id == other.employee_id

    def mark_send(self, send_at: datetime | None = None) -> None:
        if self._sent_at is not None:
            raise AlreadySentError("the letter has already been sent")
        self._sent_at = send_at if send_at is not None else datetime.now(UTC)
        self._recalculate_risk_score()

    def mark_opened(self, mark_opened_at: datetime | None = None) -> None:
        if self._sent_at is None:
            raise NotSentYetError("you cannot open a letter that has not yet been sent")
        if self._opened_at is not None:
            raise AlreadyOpenedError("the letter has already been opened")
        self._opened_at = mark_opened_at if mark_opened_at is not None else datetime.now(UTC)
        self._recalculate_risk_score()

    def mark_clicked(self, mark_clicked_at: datetime | None = None) -> None:
        if self._sent_at is None:
            raise NotSentYetError("you cannot open a letter that has not yet been sent")
        self._clicked_at.append(mark_clicked_at if mark_clicked_at is not None else datetime.now(UTC))
        self._recalculate_risk_score()

    def mark_credentials_submitted(self, mark_credentials_submitted_at: datetime | None = None) -> None:
        if self._sent_at is None:
            raise NotSentYetError("you cannot open a letter that has not yet been sent")
        if self._opened_at is None:
            raise NotOpenedYetError("The letter was not opened")
        self._submitted_credentials_at.append(mark_credentials_submitted_at) if mark_credentials_submitted_at is not None\
            else self._submitted_credentials_at.append(datetime.now(UTC))
        self._recalculate_risk_score()

    @property
    def sent_at(self) -> datetime | None:
        return self._sent_at

    @property
    def opened_at(self) -> datetime | None:
        return self._opened_at

    @property
    def clicked_at(self) -> tuple:
        return tuple(self._clicked_at)

    @property
    def risk_score(self) -> float:
        return self._risk_score

    @property
    def count_submitted_credentials_at(self) -> int:
        return len(self._submitted_credentials_at)

    def _recalculate_risk_score(self) -> None:
        self._risk_score = self._calculate_risk_score()

    def _calculate_risk_score(self) -> float:
        sent_score = 0.1
        opened_score = 0.3
        first_click_score = 0.3
        additional_clicks_score = 0.05
        max_additional_score = 0.1
        max_score = 1.0
        current_score = 0.0

        if self._sent_at is None:
            return 0.0
        current_score += sent_score

        if self._opened_at is not None:
            current_score += opened_score
        clicks_count = len(self._clicked_at)
        if clicks_count > 0:
            current_score += first_click_score
        if clicks_count > 1:
            additional_clicks = clicks_count - 1
            additional_total = min(additional_clicks * additional_clicks_score, max_additional_score)
            current_score += additional_total

        if self.count_submitted_credentials_at > 0:
            return 1.0

        return min(current_score, max_score)
