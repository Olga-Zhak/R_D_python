import requests
from faker import Faker
fake = Faker()
from pytest_steps import test_steps
credentions = {"Authorization": "pk_194448192_K8TF4EQBGZS7DZJ2GKEXBKRL7O44LJ8A"}
credention_wrong = {"Authorization": "invalid_token"}

def test_get_goals():
    result = requests.get("https://api.clickup.com/api/v2/team/90151152155/goal", headers=credention_wrong)
    assert result.status_code == 401
    print(result.text)

def test_create_goal():
    body = {
        "name": fake.first_name()
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151152155/goal", headers=credentions, json=body)
    print(result.json()['goal']['id'])
    assert result.status_code == 200

def test_get_goal_by_id():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151152155/goal", headers=credentions, json=body)
    goal_id = result.json()['goal']['id']

    result = requests.get("https://api.clickup.com/api/v2/goal/" + goal_id, headers=credentions)
    assert result.status_code == 200


def test_update_goal():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151152155/goal", headers=credentions, json=body)
    goal_id = result.json()['goal']['id']

    random_name_updated = fake.first_name()
    body_updated = {
        "name": fake.first_name()
    }
    result = requests.put("https://api.clickup.com/api/v2/goal/" + goal_id, headers=credentions, json=body_updated)
    assert result.status_code == 200

@test_steps("Create new goal", "Delete the goal")
def test_delete_goal():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151152155/goal", headers=credentions, json=body)
    goal_id = result.json()['goal']['id']
    yield
    result = requests.delete("https://api.clickup.com/api/v2/goal/" + goal_id, headers=credentions)
    assert result.status_code == 200
    yield