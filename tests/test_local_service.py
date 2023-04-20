from settings import LOCAL_API_URL
from unittest.mock import patch
import json
import requests

######## TEST FOR SERVICE USERS ########

def test_users():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5000
    assert response.json()[0]['name'] == 'Ms. Jailyn Reichert MD'
    assert response.json()[0]['email'] == "elbert@example.org"
    assert response.json()[0]['id'] == '00000000-0000-0000-0000-000000000001'


def test_user_health_200():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'] + '/health', headers=headers)
    assert response.status_code == 200
    assert response.json()["healthy"] == True


def test_get_user():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['user'] + '/00000000-0000-0000-0000-000000000427', headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Ms. Kaycee Bauch DVM'
    assert response.json()['email'] == 'pollich.mandy@example.org'


######## TEST FOR SERVICE TICKETS ########
LOCAL_API_URL['ticket'] = "http://127.0.0.1:5000/api/v1/tickets"

def test_get_all_tickets():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert "id" in response.json()[0]
    assert "concert" in response.json()[0]
    assert "user" in response.json()[0]
    assert "print_status" in response.json()[0]


def test_get_all_tickets_with_filters_1():
    # Given valid user_id and concert_id
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'] + "?user_id=00000000-0000-0000-0000-000000000001&concert_id=278d830e-12ad-4348-875c-a9185a3eaafa", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == '6cb2ce8f-5411-40be-ab50-20f3e9fd3ce9'
    assert response.json()[0]['print_status'] == 'NOT_PRINTED'


def test_get_all_tickets_with_filters_2():
    # Given valid user_id and no concert_id
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'] + "?user_id=00000000-0000-0000-0000-000000000010", headers=headers)
    a = response.json()
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['id'] == '60d5af24-2039-437e-a76c-5b57da7a4044'
    assert response.json()[1]['id'] == 'a618c09c-a4a0-418c-a9f6-ee11b849a145'
    assert response.json()[0]['print_status'] == 'NOT_PRINTED'


def test_get_all_tickets_with_filters_3():
    # Given no user_id and valid concert id
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'] + "?concert_id=278d830e-12ad-4348-875c-a9185a3eaafa", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]['print_status'] == 'NOT_PRINTED'
    assert response.json()[0]['concert']['id'] == '278d830e-12ad-4348-875c-a9185a3eaafa'
    assert response.json()[0]['user']['id'] == '00000000-0000-0000-0000-000000000007'

    for ticket in response.json():
        assert 'id' in ticket
        assert 'concert' in ticket
        assert 'user' in ticket
        assert 'print_status' in ticket


def test_get_all_tickets_with_filters_4():
    headers = {'Accept': 'application/json'}
    # Given invalid user_id
    response = requests.get(LOCAL_API_URL['ticket'] + "?user_id=00000000-0000-0000-0f00-000000000010", headers=headers)
    assert response.status_code == 404
    # given invalid concert_id
    response = requests.get(LOCAL_API_URL['ticket'] + "?concert_id=278ds30e-12ad-4348-875c-a9185a3saaf2", headers=headers)
    assert response.status_code == 404
    # given both invalid user_id and invalid concert_id
    response = requests.get(LOCAL_API_URL['ticket'] + "?user_id=00000000-00f0-0000-0000-000000000001&concert_id=2s8d830e-12ad-4348-875c-a9185a3eaafa", headers=headers)
    assert response.status_code == 404
    # given invalid para. price
    response = requests.get(LOCAL_API_URL['ticket'] + "?price_id=00000000-00f0-0000-0000-000000000001", headers=headers)
    a = response.json()
    assert response.status_code == 404
    # given one valid para and mutiple invalid para
    response = requests.get(LOCAL_API_URL['ticket'] + "?price_id=00000000-00f0-0000-0000-000000000001&user_id=00000000-0000-0000-0000-000000000010", headers=headers)
    a = response.json()
    assert response.status_code == 404
    


def test_create_ticket_1():
    # valid user_id and invalid_userid
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "concert_id": "5b52956d-d476-40d1-9acd-704465e839be",
        "user_id": "00000000-0000-0000-0000-000000000019"
    }
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["concert"]['id'] == "5b52956d-d476-40d1-9acd-704465e839be"
    assert response.json()["user"]['id'] == "00000000-0000-0000-0000-000000000019"
    assert response.json()["print_status"] == "NOT_PRINTED"

def test_create_ticket_2():
    # create ticket with invalid user_id and valid concert_id
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "concert_id": "5b52956d-d476-40d1-9acd-704465ed39be",
        "user_id": "00000000-0000-0000-0000-000000000019"
    }
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 400
    # valid user_id and invlida concert_id
    data = {
        "concert_id": "5b52956d-d476-40d1-9acd-704465e839be",
        "user_id": "10000000-0000-0000-0000-000000000019"
    }
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 400


# todo
def test_create_ticket_3():
    # random insert another 9 tickets
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "concert_id": "dcccd0e5-532c-4099-a71c-7ddbed0b1a23",
        "user_id": "00000000-0000-0000-0000-000000000019"
    }
    for i in range(9):
        response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
        assert response.status_code == 200
    
    # the number of tickets in this concert should be 10
    response = requests.get(LOCAL_API_URL['ticket'] + "?concert_id=dcccd0e5-532c-4099-a71c-7ddbed0b1a23", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 10

    # try to create another ticket for this concert
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 400


def test_create_ticket_missing_data():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "concert_id": "00000000-0000-0000-0000-000000000002"
    }
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 400

def test_create_ticket_invalid_concert_or_user():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "concert_id": "00000000-0000-0000-0000-000000000999",
        "user_id": "00000000-0000-0000-0000-000000000001"
    }
    response = requests.post(LOCAL_API_URL['ticket'], headers=headers, data=json.dumps(data))
    assert response.status_code == 400

def test_get_ticket_by_id():
    # get a valid ticket id by call /tickets
    headers = {'Accept': 'application/json'}
    ticket_id = "4f0ba636-0d70-47a8-bd3e-b3288c60e407"
    response = requests.get(LOCAL_API_URL['ticket'] + f"/{ticket_id}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "concert" in response.json()
    assert "user" in response.json()
    assert "print_status" in response.json()
    assert response.json()["id"] == ticket_id
    assert response.json()["concert"]['id'] == "198ddd71-5279-4e1c-b492-ea46614b9a73"
    assert response.json()["user"]['id'] == "00000000-0000-0000-0000-000000000008"

def test_get_ticket_by_id_not_found():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'] + "/non-existent-ticket-id", headers=headers)
    assert response.status_code == 404
    assert "error" in response.json()

def test_ticket_health_200():
    headers = {'Accept': 'application/json'}
    response = requests.get(LOCAL_API_URL['ticket'] + '/health', headers=headers)
    assert response.status_code == 200
    a = response.json()
    assert response.json()["healthy"] == True


def test_print_ticket_1():
    # valid ticket id and un-printed
    pass

def test_print_ticket_2():
    # valid ticket id, pending
    pass

def test_print_ticket_3():
    # valid ticket id, error
    pass

def test_print_ticket_4():
    # valid ticket id, printed
    pass

def test_print_ticket_5():
    # not valid ticket
    pass
