import unittest
import requests
import time
from xml.etree import ElementTree
from pprint import pprint
from .base import BaseCase


class TestConcert(BaseCase):
    example = {
        'name': 'The Beatles',
        'venue': 'The Gabba',
        'date': '2023-06-07',
        'capacity': 250,
        'status': 'ACTIVE'
    }

    def get_seating_plan(self, concert_id, expected, timeout=3) -> str:
        """
        Get the seating plan for a concert, retrying until the expected description is returned
        :param concert_id:
        :param expected:
        :param timeout:
        :return:
        """
        timeout = time.time() + (60 * timeout) + 30  # 30 seconds to account for the time it takes to test the output
        while time.time() <= timeout:
            response = requests.get(self.host() + '/concerts/' + concert_id + '/seats')

            if time.time() > timeout:
                self.fail("Seating plan was not available in time")

            if response.status_code != 200:
                continue

            print(response.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(response.headers['Content-Type'], 'image/svg+xml')

            try:
                tree = ElementTree.fromstring(response.content)
                description = tree.find('{http://www.w3.org/2000/svg}desc')
                if description.text == expected:
                    return description.text
            except ElementTree.ParseError:
                continue

        self.fail('Seating plan not updated')

    def test_concerts_health(self):
        response = requests.get(self.host() + '/concerts/health',
                                headers={'Accept': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_create_concert(self):
        response = requests.post(self.host() + '/concerts',
                                 headers={'Accept': 'application/json'},
                                 json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

    def test_create_invalid_concert(self):
        # Empty date
        response = requests.post(self.host() + '/concerts',
                                 headers={'Accept': 'application/json'},
                                 json={
                                     'name': 'The Beatles',
                                     'venue': 'The Gabba',
                                     'date': '',
                                     'capacity': 250,
                                     'status': 'ACTIVE'
                                 })
        self.assertEqual(400, response.status_code)

        # Negative Capacity
        response = requests.post(self.host() + '/concerts',
                                 headers={'Accept': 'application/json'},
                                 json={
                                     'name': 'The Beatles',
                                     'venue': 'The Gabba',
                                     'date': '2023-06-07',
                                     'capacity': -1,
                                     'status': 'ACTIVE'
                                 })
        self.assertEqual(400, response.status_code)

        # Invalid status
        response = requests.post(self.host() + '/concerts',
                                 headers={'Accept': 'application/json'},
                                 json={
                                     'name': 'The Beatles',
                                     'venue': 'The Gabba',
                                     'date': '2023-06-07',
                                     'capacity': 250,
                                     'status': 'INVALID'
                                 })
        self.assertEqual(400, response.status_code)

    def test_create_missing_concert(self):
        # No Fields
        response = requests.post(self.host() + '/concerts', json={})
        self.assertEqual(400, response.status_code)

        # Missing name
        response = requests.post(self.host() + '/concerts', json={
            'venue': 'The Gabba',
            'date': '2023-06-07',
            'capacity': 250,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

        # Missing venue
        response = requests.post(self.host() + '/concerts', json={
            'name': 'The Beatles',
            'date': '2023-06-07',
            'capacity': 250,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

        # Missing date
        response = requests.post(self.host() + '/concerts', json={
            'name': 'The Beatles',
            'venue': 'The Gabba',
            'capacity': 250,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

        # Missing capacity
        response = requests.post(self.host() + '/concerts', json={
            'name': 'The Beatles',
            'venue': 'The Gabba',
            'date': '2023-06-07',
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

    def test_get_concert(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.get(self.host() + '/concerts/' + response.json()['id'])
        self.assertEqual(200, response.status_code)
        self.assertEqual(concert, response.json())

    def test_list_concerts(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.get(self.host() + '/concerts')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, len(response.json()) > 0)

        self.assertIn(concert, response.json())

    def test_update_concert_status(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'CANCELLED'
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual('CANCELLED', response.json()['status'])

        response = requests.get(self.host() + '/concerts/' + concert['id'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('CANCELLED', response.json()['status'])

    def test_update_concert_name(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': 'The Rolling Stones'
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual('The Rolling Stones', response.json()['name'])

        response = requests.get(self.host() + '/concerts/' + concert['id'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('The Rolling Stones', response.json()['name'])

    def test_update_concert_venue(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'venue': 'The MCG'
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual('The MCG', response.json()['venue'])

        response = requests.get(self.host() + '/concerts/' + concert['id'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('The MCG', response.json()['venue'])

    def test_update_concert_date(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'date': '2023-06-08'
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual('2023-06-08', response.json()['date'])

        response = requests.get(self.host() + '/concerts/' + concert['id'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('2023-06-08', response.json()['date'])

    def test_update_concert_all(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': 'The Rolling Stones',
            'venue': 'The MCG',
            'date': '2023-06-08',
            'status': 'CANCELLED'
        })
        self.assertEqual(200, response.status_code)
        self.assertDictSubset({
            'name': 'The Rolling Stones',
            'venue': 'The MCG',
            'date': '2023-06-08',
            'status': 'CANCELLED'
        }, response.json())

        response = requests.get(self.host() + '/concerts/' + concert['id'])
        self.assertEqual(200, response.status_code)
        self.assertDictSubset({
            'name': 'The Rolling Stones',
            'venue': 'The MCG',
            'date': '2023-06-08',
            'status': 'CANCELLED'
        }, response.json())

    def test_update_concert_capacity(self):
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'capacity': 300
        })
        self.assertEqual(400, response.status_code)

    def test_update_concert_that_does_not_exist(self):
        response = requests.put(self.host() + '/concerts/999999999', json={
            'name': 'The Rolling Stones'
        })
        self.assertEqual(404, response.status_code, "Should return a 404 if the concert does not exist or "
                                                    "if the ID is invalid")

    def test_seating_plan(self):
        """
        Checks that a concerts seating plan
        :return:
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())

        concert = response.json()
        # print(concert)
        description = self.get_seating_plan(concert['id'], f'{concert["id"]}|{concert["capacity"]}|0')
        print(description)
        self.assertEqual(f'{concert["id"]}|{concert["capacity"]}|0', description)

    def test_seating_update_tickets(self):
        """
        This test will perform the following steps:

        1) Create a concert
        2) Get the seating plan
        3) purchase a ticket
        4) wait 3 minutes
        5) get the seating plan again
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())
        concert = response.json()

        pprint(concert)
        description = self.get_seating_plan(concert['id'], f'{concert["id"]}|{concert["capacity"]}|0')
        self.assertEqual(f'{concert["id"]}|{concert["capacity"]}|0', description)

        # purchase a ticket
        response = requests.post(self.host() + '/tickets', json={
            'concert_id': concert['id'],
            'user_id': '00000000-0000-0000-0000-000000000001'
        })
        self.assertEqual(201, response.status_code)

        # get the seating plan again
        # description = self.get_seating_plan(concert['id'], f'{concert["id"]}|{concert["capacity"]}|1')
        # self.assertEqual(f'{concert["id"]}|{concert["capacity"]}|1', description)

    def test_clearing_tickets(self):
        """
        This test will perform the following steps:

        1) Create a concert
        2) Create a ticket for that concert
        3) Print the ticket
        4) Update the concert details
        5) Check that the ticket has no printed version
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())
        concert = response.json()

        response = requests.post(self.host() + '/tickets', json={
            'user_id': '00000000-0000-0000-0000-000000000001',
            'concert_id': concert['id'],
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']
        self.assertDictSubset({
            'print_status': 'NOT_PRINTED'
        }, response.json())

        response = requests.post(self.host() + '/tickets/' + ticket_id + '/print')
        self.assertEqual(202, response.status_code)

        response = requests.get(self.host() + '/tickets/' + ticket_id)
        status = response.json()['print_status']
        self.assertIn(status, ['PRINTED', 'PENDING'])

        # timeout after 3 minutes
        # todo(eh): fix this to be proper time not sudo time
        for i in range(0, 180):
            response = requests.get(self.host() + '/tickets/' + ticket_id)
            self.assertEqual(200, response.status_code)
            status = response.json()['print_status']
            if status == 'PRINTED':
                break
            time.sleep(1)

        status = response.json()['print_status']
        self.assertEqual('PRINTED', status)

        # update the concert
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'CANCELLED'
        })
        self.assertEqual(200, response.status_code)
        self.assertDictSubset({
            'status': 'CANCELLED'
        }, response.json())

        # check that the ticket has no printed version
        response = requests.get(self.host() + '/tickets/' + ticket_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual('NOT_PRINTED', response.json()['print_status'])

        response = requests.get(self.host() + '/tickets/' + ticket_id + '/print')
        self.assertEqual(404, response.status_code)

    def test_update_concert_influence_tickets(self):
        """
        Update a concert and check that the tickets are updated
        :return:
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        concert = response.json()

        tickets = []
        # Buy 5 tickets for the concert and print them
        for i in range(0, 2):
            response = requests.post(self.host() + '/tickets', json={
                'user_id': '00000000-0000-0000-0000-000000000001',
                'concert_id': concert['id'],
            })
            self.assertEqual(201, response.status_code)
            ticket_id = response.json()['id']
            tickets.append(response.json())
            response = requests.post(self.host() + '/tickets/' + ticket_id + '/print')
            self.assertEqual(202, response.status_code)
            # save the ticket in tickets

        print(tickets)
        # Loop for up to 50 seconds until all tickets are printed
        start_time = time.time()
        while time.time() - start_time < 50:
            all_printed = True
            for ticket in tickets:
                response = requests.get(self.host() + '/tickets/' + ticket['id'])
                self.assertEqual(200, response.status_code)
                ticket_status = response.json()['print_status']
                if ticket_status != 'PRINTED':
                    all_printed = False
                    break
            if all_printed:
                print("All tickets printed.")
                break
            time.sleep(1)  # Wait a second before checking again

        # updated the concert
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'CANCELLED'
        })

        # check that tickets' print_status is NOT_PRINTED
        for ticket in tickets:
            response = requests.get(self.host() + '/tickets/' + ticket['id'])
            print("\n\n")
            print(response.json())
            self.assertEqual(200, response.status_code)
            self.assertEqual('NOT_PRINTED', response.json()['print_status'])

    def test_no_extra_keys(self):
        """
        Response only contain key:
        id, name, venue, date, capacity, status, status
        :param self:
        :return:
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        self.assertDictSubset(self.example, response.json())
        concert = response.json()
        self.assertEqual(len(concert), 6)
        valid_keys = ['id', 'name', 'venue', 'date', 'capacity', 'status']
        for key in concert:
            self.assertIn(key, valid_keys)

    def test_create_new_concert_with_extra_values(self):
        """
        Create a new concert with name, venue, date, capacity, status, invalid_field
        :return:
        """
        response = requests.post(self.host() + '/concerts', json={
            'name': 'test',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 100,
            'status': 'OPEN',
            'invalid_field': 'test'
        })
        self.assertEqual(400, response.status_code)

    def test_create_with_missing_value(self):
        """
        Create a new concert with name, venue, date, capacity, status, invalid_field
        :return:
        """
        response = requests.post(self.host() + '/concerts', json={
            'name': 'test',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 100,
        })
        self.assertEqual(400, response.status_code)

    def test_create_with_invalid_value(self):
        """
        build 6 request with invalid value in each field.
        Fields:" id, name, venue, date, capacity, status
        :return:
        """
        # invalid id
        response = requests.post(self.host() + '/concerts', json={
            'id': 'invalid_id',
            'name': 'test',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 100,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

    def test_create_with_invalid_date(self):
        """
        :return:
        """
        # invalid id
        response = requests.post(self.host() + '/concerts', json={
            'name': 'test',
            'venue': 'test',
            'date': '2018-01-01 00:00:00',
            'capacity': 100,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

        response = requests.post(self.host() + '/concerts', json={
            'name': 'test',
            'venue': 'test',
            'date': '2022-00-01',
            'capacity': 100,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

        response = requests.post(self.host() + '/concerts', json={
            'name': 'test',
            'venue': 'test',
            'date': '2022-30-12',
            'capacity': 100,
            'status': 'ACTIVE'
        })
        self.assertEqual(400, response.status_code)

    def test_update_invalid_field(self):
        """
        invalids filed are concert_id, and capacity
        :return:
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': 'test',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 100,
            'status': 'ACTIVE',
            'invalid_field': 'test'
        })
        self.assertEqual(400, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'id': '00000000-0000-0000-0000-000000000001'
        })
        self.assertEqual(400, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'capacity': 100
        })
        self.assertEqual(400, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'date': '2018-01-01 00:00:00'
        })
        self.assertEqual(400, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'date': '2022-00-01'
        })
        self.assertEqual(400, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'INVALID_STATUS'
        })
        self.assertEqual(400, response.status_code)

    def test_update_with_valid_status(self):
        """
        :return:
        """
        response = requests.post(self.host() + '/concerts', json=self.example)
        self.assertEqual(201, response.status_code)
        concert = response.json()

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'CANCELLED'
        })
        self.assertEqual(200, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'ACTIVE'
        })
        self.assertEqual(200, response.status_code)

        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'status': 'SOLD_OUT'
        })
        self.assertEqual(200, response.status_code)

    def test_update_with_unexist_id(self):
        """
        :return:
        """
        response = requests.put(self.host() + '/concerts/00000000-0000-0000-0000-000000000001', json={
            'status': 'CANCELLED'
        })
        self.assertEqual(404, response.status_code)

    ### SEATING GENERATION TESTS
    def test_svg_create_order_test(self):
        # create a concert with 10 seats
        response = requests.post(self.host() + '/concerts', json={
            'name': '10 Seats',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 10,
            'status': 'ACTIVE'
        })

        self.assertEqual(201, response.status_code)

        # create 9 tickets in this concert
        concert = response.json()
        for i in range(5):
            response = requests.post(self.host() + '/tickets', json={
                'user_id': "00000000-0000-0000-0000-000000000003",
                'concert_id': concert['id'],
            })
            self.assertEqual(201, response.status_code)

    def test_svg_change_concert_info(self):
        # create a concert with 10 seats
        response = requests.post(self.host() + '/concerts', json={
            'name': '10 Seats',
            'venue': 'test',
            'date': '2018-01-01',
            'capacity': 10,
            'status': 'ACTIVE'
        })
        self.assertEqual(201, response.status_code)

        # change name of concert
        concert = response.json()
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': '1 Seats'
        })
        self.assertEqual(200, response.status_code)

        concert = response.json()
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': '1 Seats'
        })
        self.assertEqual(200, response.status_code)

        concert = response.json()
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': '2 Seats'
        })
        self.assertEqual(200, response.status_code)

        concert = response.json()
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': '3 Seats'
        })
        self.assertEqual(200, response.status_code)

        concert = response.json()
        response = requests.put(self.host() + '/concerts/' + concert['id'], json={
            'name': '4 Seats'
        })
        self.assertEqual(200, response.status_code)
