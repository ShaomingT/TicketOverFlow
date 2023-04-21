from settings import CURR_URLS
import requests
import time
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import logging
import sys


# randomly generate concert info
def generate_concert():
    return {
        "name": f"Concert {random.randint(1, 1000)}",
        "date": f"{random.randint(2000, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}",
        "venue": f"Venue {random.randint(1, 1000)}",
        "capacity": random.randint(1, 1000),
        "status": "ACTIVE"
    }




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


# def test_generate_svg_1():
#     headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
#     #create_a_concert
#     response = requests.post(CURR_URLS['concert'], headers=headers, json={
#         "name": "Concert 1",
#         "date": "2020-10-10",
#         "venue": "Venue 1",
#         "capacity": 1000,
#         "status": "ACTIVE"
#     })
#     assert response.status_code == 200
#     # get the id of the concert
#     concert_id = response.json()['id']
#     print("concert_id", concert_id)

#     # get the id of the concert
#     response = requests.get(f"{CURR_URLS['concert']}/{concert_id}/seats", headers=headers)
#     assert response.status_code == 404

#     #wait for 20 seconds, and fetch again
#     time.sleep(20)
#     response = requests.get(f"{CURR_URLS['concert']}/{concert_id}/seats", headers=headers)
#     assert response.status_code == 200


###### SETVICE TICKET TESTS ####

def helper_random_get_one_user():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    # randommal select one user
    user = random.choice(response.json())
    return user

def helper_random_get_one_concert():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['concert'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    # randommal select one user
    concert = random.choice(response.json())
    return concert

def test_ticket_health_status_200():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['ticket'] + '/health', headers=headers)
    assert response.status_code == 200
    assert response.json()["healthy"] == True


def test_get_all_tickets():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['ticket'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

# test create tickets
def test_create_ticket():
    concert = helper_random_get_one_concert()
    user = helper_random_get_one_user()

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['ticket'], headers=headers, json={
        "concert_id": concert['id'],
        "user_id": user['id'],
    })
    assert response.status_code == 200
    data = response.json()
    assert data['concert']['id'] == concert['id']
    # assert data['concert']['url'] == f"{CURR_URLS['concert']}/{concert['id']}"
    assert data['user']['id'] == user['id']
    # assert data['user']['url'] == f"{CURR_URLS['user']}/{user['id']}"
    assert data['print_status'] == 'NOT_PRINTED'

    # get the ticket by id
    response = requests.get(f"{CURR_URLS['ticket']}/{data['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == data['id']
    assert response.json()['concert']['id'] == concert['id']
    assert response.json()['user']['id'] == user['id']
    assert response.json()['print_status'] == 'NOT_PRINTED'


def helper_random_generate_one_ticket():
    concert = helper_random_get_one_concert()
    user = helper_random_get_one_user()

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    #create_a_concert
    response = requests.post(CURR_URLS['ticket'], headers=headers, json={
        "concert_id": concert['id'],
        "user_id": user['id'],
    })
    print(response.content)
    assert response.status_code == 200
    data = response.json()
    return data

def test_get_all_tickets_with_filters_1():
    data = helper_random_generate_one_ticket()

    # given valid user_id and concert_id
    headers = {'Accept': 'application/json'}
    response = requests.get(f"{CURR_URLS['ticket']}?user_id={data['user']['id']}&concert_id={data['concert']['id']}", headers=headers)
    # assert response.status_code == 200
    # the response's concert_id and user_id should be the same as the given
    assert response.json()[0]['concert']['id'] == data['concert']['id']
    assert response.json()[0]['user']['id'] == data['user']['id']


def test_get_all_tickets_with_filters_2():
    # given valid user_id but no concert_id
    data = helper_random_generate_one_ticket()
    headers = {'Accept': 'application/json'}
    response = requests.get(f"{CURR_URLS['ticket']}?user_id={data['user']['id']}", headers=headers)
    assert response.status_code == 200
    # the response's concert_id and user_id should be the same as the given
    assert response.json()[0]['concert']['id'] == data['concert']['id']
    assert response.json()[0]['user']['id'] == data['user']['id']

def test_get_all_tickets_with_filters_3():
    # given no user_id but valid concert_id
    data = helper_random_generate_one_ticket()
    headers = {'Accept': 'application/json'}
    response = requests.get(f"{CURR_URLS['ticket']}?concert_id={data['concert']['id']}", headers=headers)
    assert response.status_code == 200
    # the response's concert_id and user_id should be the same as the given
    assert response.json()[0]['concert']['id'] == data['concert']['id']
    assert response.json()[0]['user']['id'] == data['user']['id']
    

def test_get_all_tickets_with_filters_4():
    headers = {'Accept': 'application/json'}
    # Given invalid user_id
    response = requests.get(CURR_URLS['ticket'] + "?user_id=00000000-0000-0000-0f00-000000000010", headers=headers)
    assert response.status_code == 404
    # given invalid concert_id
    response = requests.get(CURR_URLS['ticket'] + "?concert_id=278ds30e-12ad-4348-875c-a9185a3saaf2", headers=headers)
    assert response.status_code == 404
    # given both invalid user_id and invalid concert_id
    response = requests.get(CURR_URLS['ticket'] + "?user_id=00000000-00f0-0000-0000-000000000001&concert_id=2s8d830e-12ad-4348-875c-a9185a3eaafa", headers=headers)
    assert response.status_code == 404
    # given invalid para. price
    response = requests.get(CURR_URLS['ticket'] + "?price_id=00000000-00f0-0000-0000-000000000001", headers=headers)
    assert response.status_code == 404
    # given one valid para and mutiple invalid para
    response = requests.get(CURR_URLS['ticket'] + "?price_id=00000000-00f0-0000-0000-000000000001&user_id=00000000-0000-0000-0000-000000000010", headers=headers)
    a = response.json()
    assert response.status_code == 404


# when concert is full, no more ticket can be sold, and the concert status should be updated
def test_full_ticket_test():
    # create a concert with 10 seats
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
            "name": "Concert 1",
            "date": "2020-10-10",
            "venue": "Venue 1",
            "capacity": 10,
            "status": "ACTIVE"
    })
    print(response.content)
    assert response.status_code == 200
    # create 10 tickets to this concert
    concert = response.json()
    for i in range(10):
        response = requests.post(CURR_URLS['ticket'], headers=headers, json={
            "concert_id": concert['id'],
            "user_id": helper_random_get_one_user()['id'],
        })
        assert response.status_code == 200
    # create 11th ticket to this concert
    response = requests.post(CURR_URLS['ticket'], headers=headers, json={
        "concert_id": concert['id'],
        "user_id": helper_random_get_one_user()['id'],
    })
    assert response.status_code == 400

    # the concert status should be marked as SOLD_OUT
    response = requests.get(f"{CURR_URLS['concert']}/{concert['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()['status'] == 'SOLD_OUT'
    return concert

def test_full_ticket_test_2():
    # create a concert with 10 seats
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(CURR_URLS['concert'], headers=headers, json={
            "name": "Concert 1",
            "date": "2020-10-10",
            "venue": "Venue 1",
            "capacity": 10,
            "status": "ACTIVE"
    })
    print(response.content)
    assert response.status_code == 200

    # create 9 tickets to this concert
    concert = response.json()
    for i in range(9):
        response = requests.post(CURR_URLS['ticket'], headers=headers, json={
            "concert_id": concert['id'],
            "user_id": helper_random_get_one_user()['id'],
        })
        assert response.status_code == 200
    # check the concert status which should be ACTIVE
    response = requests.get(f"{CURR_URLS['concert']}/{concert['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()['status'] == 'ACTIVE'
    
        

# test get all concert
def test_get_all_concert_post():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['concert'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

# test get all ticket (post)
def test_get_all_ticket_post():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['ticket'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_all_users_post():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['user'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def helper_random_get_one_ticket():
    headers = {'Accept': 'application/json'}
    response = requests.get(CURR_URLS['ticket'], headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    return random.choice(response.json())


# ticket print test
def test_ticket_print():
    # random get one ticket
    ticket = helper_random_get_one_ticket()
    # print ticket id
    print(ticket['id'])

    # print the ticket
    headers = {'Accept': 'application/json'}
    response = requests.post(f"{CURR_URLS['ticket']}/{ticket['id']}/print", headers=headers)
    assert response.status_code == 202

    # get the ticket by id
    response = requests.get(f"{CURR_URLS['ticket']}/{ticket['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()['print_status'] == 'PENDING'

    # GET /tickets/{id}/print, with response status 404. id is previous id
    response = requests.get(f"{CURR_URLS['ticket']}/{ticket['id']}/print", headers=headers)
    assert response.status_code == 404