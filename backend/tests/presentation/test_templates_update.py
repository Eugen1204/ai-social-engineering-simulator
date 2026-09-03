from uuid import uuid4

from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_template
from social_engineering_simulator.presentation.main import app
from social_engineering_simulator.domain.email_template.entity import Template


def test_update_template(client_with_repos, created_template):
    assert created_template['version'] == 1

    client, _, _ = client_with_repos
    response = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                            json={"content": "new content",
                                  "subject": None})

    print(response.json())
    assert response.status_code == 200

    assert response.json()['version'] == 2

    wrong_response = client.patch(f"organizations/{uuid4()}/templates/{created_template['id']}",
                                  json={"content": "new content",
                                        "subject": None})

    assert wrong_response.status_code == 404

    wrong_response_2 = client.patch(
        f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
        json={"content": "new content",
              "subject": ""})

    assert wrong_response_2.status_code == 400

    response_3 = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                              json={"content": None})

    assert response_3.json()['version'] == 2

    response_4 = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                              json={"content": "new vers"})

    assert response_4.json()['version'] == 3


def test_campaign_keeps_template_snapshot_after_template_update(client_with_repos, created_template, created_campaign):
    client, template_repo, _ = client_with_repos

    assert created_template['version'] == 1

    assert created_campaign['template_version'] == 1

    response = client.patch(f"/organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                            json={
                                "content": "new content",
                                "subject": None
                            })

    assert response.json()['version'] == 2

    campaign_response = client.get(f"/campaigns/{created_campaign['id']}")
    updated_campaign = campaign_response.json()

    print(updated_campaign)

    assert updated_campaign['template_version'] == 1

    new_campaign_response = client.post("/campaigns/", json={
        "name": "New Campaign",
        "organization_id": created_template['organization_id'],
        "template_id": created_template['id'],
        "landing_page_id": str(uuid4())
    })
    assert new_campaign_response.status_code == 201
    assert new_campaign_response.json()['template_version'] == 2
