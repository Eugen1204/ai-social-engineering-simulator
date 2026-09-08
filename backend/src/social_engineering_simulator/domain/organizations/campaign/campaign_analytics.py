from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class CampaignAnalytic:
    campaign_id: UUID
    total_employees: int
    sent_count: int
    opened_count: int
    clicked_employee_count: int
    credential_submission_employee_count: int
    average_risk_score: float | None

    @property
    def open_rate(self) -> float | None:
        return self._calculate_open_rate()

    @property
    def click_rate(self) -> float | None:
        return self._calculate_click_rate()

    @property
    def credential_submission_rate(self) -> float | None:
        return self._calculate_credential_submission_rate()

    def _calculate_open_rate(self) -> float | None:
        if self.sent_count == 0:
            return None
        return self.opened_count / self.sent_count

    def _calculate_click_rate(self) -> float | None:
        if self.sent_count == 0:
            return None
        return self.clicked_employee_count / self.sent_count

    def _calculate_credential_submission_rate(self) -> float | None:
        if self.sent_count == 0:
            return None
        return self.credential_submission_employee_count / self.sent_count

