def test_get_emp_timeline(client_with_repos, created_organization, created_campaign_with_emp, created_campaign,
                          created_employee):
    client, _, repo_org, repo_events, repo_campaign = client_with_repos

    campaign_id = created_campaign['id']

    client.post(f"campaigns/{campaign_id}/start")

    employee_id = created_employee['id']

    response = client.get(f"campaigns/{campaign_id}/employees/{employee_id}/timeline",
                          params={"org_id": created_organization['id']})

    assert response.status_code == 200

    assert response.json() == []
