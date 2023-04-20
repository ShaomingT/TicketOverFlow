from settings import LOCAL_API_URL



import requests

def test_users():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5000
    assert response.json()[0]['name'] == 'Ms. Jailyn Reichert MD'
    assert response.json()[0]['email'] == "elbert@example.org"
    assert response.json()[0]['id'] == '00000000-0000-0000-0000-000000000001'


def test_user_health():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'] + '/health', headers=headers)
    
    assert response.status_code == 200
    assert 'healthy' in response.json()
    assert response.json()['healthy'] == True
    assert 'dependencies' in response.json()
    assert len(response.json()['dependencies']) > 0

    for dependency in response.json()['dependencies']:
        assert 'name' in dependency
        assert 'healthy' in dependency
        assert dependency['healthy'] == True

    assert 'memoryUsage' in response.json()
    assert isinstance(response.json()['memoryUsage'], str)
    

def test_get_user():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'] + '/00000000-0000-0000-0000-000000000427', headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Ms. Kaycee Bauch DVM'
    assert response.json()['email'] == 'pollich.mandy@example.org'


