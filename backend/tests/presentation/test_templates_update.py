from uuid import uuid4

from social_engineering_simulator.infrastructure.persistence.in_memory.template_repository import \
    TemplateRepositoryInMemory
from social_engineering_simulator.presentation.api.v1.dependencies import get_repository_template
from social_engineering_simulator.presentation.main import app
from social_engineering_simulator.domain.email_template.entity import Template


def test_update_template(client_with_repos, created_template):
    assert created_template['version'] == 1

    client = client_with_repos

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

    wrong_response_2 = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                                    json={"content": "new content",
                                          "subject": ""})

    assert wrong_response_2.status_code == 400

    response_3 = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                              json={"content": None})

    assert response_3.json()['version'] == 2

    response_4 = client.patch(f"organizations/{created_template['organization_id']}/templates/{created_template['id']}",
                              json={"content": "new vers"})

    assert response_4.json()['version'] == 3
