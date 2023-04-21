from settings import CURR_URLS
import requests
import time
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed


########### SERVICE USER TESTS ###########
def test_user_health_status_200():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'] + '/health', headers=headers)
    assert response.status_code == 200
    assert response.json()["healthy"] == True


def test_get_all_users():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5000
    assert response.json()[0]['name'] == 'Ms. Jailyn Reichert MD'
    assert response.json()[0]['email'] == "elbert@example.org"
    assert response.json()[0]['id'] == '00000000-0000-0000-0000-000000000001'


def test_user_by_id():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'] + '/00000000-0000-0000-0000-000000000427', headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Ms. Kaycee Bauch DVM'
    assert response.json()['email'] == 'pollich.mandy@example.org'

def test_user_by_id_not_found():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'] + '/00000000-0000-0000-0000-000000099', headers=headers)
    assert response.status_code == 404


########### SERVICE CONCERT TESTS ###########
def test_concert_health_status_200():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['concert'] + '/health', headers=headers)
    assert response.status_code == 200
    assert response.json()["healthy"] == True


# no data is in DB now
def test_get_all_concerts():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['concert'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


# create first concerts
def test_create_concerts_1():
    headers = {'Accept': 'application/json'}
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    assert response.json()['name'] == 'Concert 1'
    assert response.json()['date'] == '2020-10-10'
    assert response.json()['venue'] == 'Venue 1'
    assert response.json()['capacity'] == 1000
    assert response.json()['status'] == 'ACTIVE'
    # make sure no other fields are added
    assert len(response.json()) == 6
    # make sure the uuid is valid
    assert len(response.json()['id']) == 36

def test_create_concerts_2():
    # test four status cases ACTIVE, CANCELLED, SOLD_OUT
    headers = {'Accept': 'application/json'}
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 2",
        "date": "2020-10-10",
        "venue": "Venue 2",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 2",
        "date": "2020-10-10",
        "venue": "Venue 2",
        "capacity": 1000,
        "status": "CANCELLED"
    })
    assert response.status_code == 200
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 2",
        "date": "2020-10-10",
        "venue": "Venue 2",
        "capacity": 1000,
        "status": "SOLD_OUT"
    })
    assert response.status_code == 200
    


def test_create_concerts_invalid_data():
    headers = {'Accept': 'application/json'}
    # invalid date
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-55",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE",
    })
    assert response.status_code == 400
    # invalid status
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "INVALID",
    })
    assert response.status_code == 400

    # miss one filed
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
    })
    assert response.status_code == 400

    # extra invalid field
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE",
        "invalid": "invalid"
    })
    assert response.status_code == 400    

def test_get_concert_by_id():
    headers = {'Accept': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    # get the id of the concert
    concert_id = response.json()['id']
    response = requests.get(f"{CURR_URLS['concert']}/{concert_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Concert 1'
    assert response.json()['date'] == '2020-10-10'
    assert response.json()['venue'] == 'Venue 1'
    assert response.json()['capacity'] == 1000
    assert response.json()['status'] == 'ACTIVE'
    # make sure no other fields are added
    assert len(response.json()) == 6
    # make sure the uuid is valid
    assert response.json()['id'] == concert_id 


def test_modify_concerts():
# test modify all fields
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    # get the id of the concert
    concert_id = response.json()['id']

    # get the id of the concert

    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "name": "Concert 2",
        "date": "2020-10-15",
        "venue": "Venue 2",
        "capacity": 123,
        "status": "CANCELLED"
    })

    assert response.status_code == 200
    assert response.json()['name'] == 'Concert 2'
    assert response.json()['date'] == '2020-10-15'
    assert response.json()['venue'] == 'Venue 2'
    assert response.json()['capacity'] == 123
    assert response.json()['status'] == 'CANCELLED'
    # make sure no other fields are added
    assert len(response.json()) == 6
    assert response.json()['id'] == concert_id


    # get the concert, wo see whethe it is changed successfully or not
    response = requests.get(f"{CURR_URLS['concert']}/{concert_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()['name'] == 'Concert 2'
    assert response.json()['date'] == '2020-10-15'
    assert response.json()['venue'] == 'Venue 2'
    assert response.json()['capacity'] == 123
    assert response.json()['status'] == 'CANCELLED'
    # make sure no other fields are added
    assert len(response.json()) == 6
    assert response.json()['id'] == concert_id


def test_modify_concerts_2():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    # get the id of the concert
    concert_id = response.json()['id']

    #try to modify id
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "id": "123"
        })
    assert response.status_code == 400

    #try to modify invalid field
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "invalid": "123"
        })
    assert response.status_code == 400

    #try to modify invalid date
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "date": "2020-10-55"
        })
    assert response.status_code == 400

    #try to modify invalid status
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "status": "INVALID"
        })
    assert response.status_code == 400

    #try to modify invalid capacity
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "capacity": -1
        })
    assert response.status_code == 400

    #try to modify invalid capacity
    response = requests.put(f"{CURR_URLS['concert']}/{concert_id}", headers=headers, json={
        "capacity": "invalid"
        })
    assert response.status_code == 400


def test_generate_svg_1():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
        "name": "Concert 1",
        "date": "2020-10-10",
        "venue": "Venue 1",
        "capacity": 1000,
        "status": "ACTIVE"
    })
    assert response.status_code == 200
    # get the id of the concert
    concert_id = response.json()['id']

    # get the id of the concert
    response = requests.get(f"{CURR_URLS['concert']}/{concert_id}/seats", headers=headers)
    assert response.status_code == 404

    #wait for 20 seconds, and fetch again
    time.sleep(20)
    response = requests.get(f"{CURR_URLS['concert']}/{concert_id}/seats", headers=headers)
    assert response.status_code == 200

    # assert response.headers['Content-Type'] == 'image/svg+xml'
    # assert response.headers['Content-Disposition'] == 'attachment; filename=Concert_1.svg'
