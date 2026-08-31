from social_engineering_simulator.application.dto.add_employee import \
    RemoveCampaignEmployeeRequest, CampaignEmployeeResponse, AddCampaignEmployeeRequest
from social_engineering_simulator.application.services.exceptions_create_campaign import CampaignNotFoundError, \
    DifferentIdError
from social_engineering_simulator.domain.organizations.campaign.repository import CampaignRepository
from social_engineering_simulator.domain.organizations.exceptions import OrganizationNotFoundError, \
    EmployeeNotFoundError
from social_engineering_simulator.domain.organizations.repository import OrganizationRepository


class AddCampaignEmployeeService:
    def __init__(self, repo_campaign: CampaignRepository, repo_org: OrganizationRepository):
        self.repo_campaign = repo_campaign
        self.repo_org = repo_org

    def execute(self, request: AddCampaignEmployeeRequest):
        campaign = self.repo_campaign.get_by_id(request.campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(f"Campaign with {request.campaign_id} not found")
        organization = self.repo_org.get_by_id(campaign.organization_id)
        if organization is None:
            raise OrganizationNotFoundError(f"Organization with {campaign.organization_id} not found")
        employee = organization.get_employee(request.employee_id)
        if employee is None:
            raise EmployeeNotFoundError(f"Employee with {request.employee_id} not found")

        campaign.assign_employee(employee.id)
        self.repo_campaign.save(campaign)

        return CampaignEmployeeResponse(name=employee.name.value, id=employee.id, email=employee.email.value,
                                        department_id=employee.department_id)


class RemoveCampaignEmployeeService:
    def __init__(self, repo_campaign: CampaignRepository):
        self.repo_campaign = repo_campaign

    def execute(self, request: RemoveCampaignEmployeeRequest):
        campaign = self.repo_campaign.get_by_id(request.campaign_id)
        if campaign is None:
            raise CampaignNotFoundError(f"Campaign with {request.campaign_id} not found")

        campaign.remove_employee(request.employee_id)
        self.repo_campaign.save(campaign)


