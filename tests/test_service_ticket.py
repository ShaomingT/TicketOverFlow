from settings import LOCAL_API_URL



import requests

def test_get_users():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    assert response.status_code == 200
    assert len(response.json()) == 10

def test_get_user():
    response = requests.get('https://jsonplaceholder.typicode.com/users/1')
    assert response.status_code == 200
    assert response.json()['name'] == 'Leanne Graham'

def test_post_user():
    data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'username': 'johndoe'
    }
    response = requests.post('https://jsonplaceholder.typicode.com/users', json=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'John Doe'
    assert response.json()['email'] == 'johndoe@example.com'
    assert response.json()['username'] == 'johndoe'

