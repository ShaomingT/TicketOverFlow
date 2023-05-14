import unittest
import requests
import time
from xml.etree import ElementTree
from pprint import pprint

from .base import BaseCase


class TestTicket(BaseCase):
    user_id = '00000000-0000-0000-0000-000000000001'
    other_user = '00000000-0000-0000-0000-000000000002'

    def createConcert(self, capacity=1) -> str:
        # create a concert
        response = requests.post(self.host() + '/concerts', json={
            'name': 'test concert',
            'venue': 'test place',
            'date': '2020-01-01',
            'capacity': capacity,
            'status': 'ACTIVE'
        })
        self.assertEqual(201, response.status_code)
        return response.json()['id']

    def test_ticket_health(self):
        response = requests.get(self.host() + '/tickets/health')
        self.assertEqual(200, response.status_code)

    def test_create_ticket(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        print(response.json())
        self.assertEqual(201, response.status_code)
        self.assertDictSubset({
            'user': {
                'id': self.user_id,
                'url': self.host() + '/users/' + self.user_id,
            },
            'concert': {
                'id': concert_id,
                'url': self.host() + '/concerts/' + concert_id,
            },
            'print_status': 'NOT_PRINTED',
        }, response.json())

    def test_create_ticket_with_invalid_user_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': 'invalid_user_id',
            'concert_id': concert_id,
        })
        self.assertEqual(400, response.status_code)

    def test_create_ticket_with_invalid_concert_id(self):
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': 'invalid_concert_id',
        })
        self.assertEqual(400, response.status_code)

    def test_purchasing_too_many_tickets(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)

        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(422, response.status_code, "Should have no tickets left for sale.")

    def test_get_ticket(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']

        response = requests.get(self.host() + '/tickets/' + ticket_id)
        self.assertEqual(200, response.status_code)
        self.assertDictSubset({
            'id': ticket_id,
            'user': {
                'id': self.user_id,
                'url': self.host() + '/users/' + self.user_id,
            },
            'concert': {
                'id': concert_id,
                'url': self.host() + '/concerts/' + concert_id,
            },
            'print_status': 'NOT_PRINTED',
        }, response.json(), )

    def test_get_ticket_with_invalid_id(self):
        response = requests.get(self.host() + '/tickets/invalid_ticket_id')
        self.assertEqual(404, response.status_code)

    def test_get_tickets_with_invalid_user_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']

        response = requests.get(self.host() + '/tickets' + '?user_id=invalid_user_id')
        self.assertEqual(404, response.status_code)

    def test_get_tickets_with_invalid_concert_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']

        response = requests.get(self.host() + '/tickets' + '?concert_id=invalid_concert_id')
        self.assertEqual(404, response.status_code)

    def test_get_tickets_with_invalid_user_id_and_concert_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']

        response = requests.get(self.host() + '/tickets' + '?user_id=invalid_user_id&concert_id=invalid_concert_id')
        self.assertEqual(404, response.status_code)

    def test_get_tickets(self):
        concert_id = self.createConcert()
        print(f"concert_id: {concert_id} \n")
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket = response.json()

        print("\n\n ticket: \n\n")
        pprint(ticket)

        response = requests.get(self.host() + '/tickets')

        print("\n\n response: \n\n")
        pprint(response.json())
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)
        self.assertIn(ticket, response.json())

    def test_get_tickets_with_user_id(self):
        concert_id = self.createConcert(capacity=2)
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket = response.json()

        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.other_user,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        other_ticket = response.json()

        response = requests.get(self.host() + '/tickets?user_id=' + self.user_id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)
        self.assertIn(ticket, response.json())
        self.assertNotIn(other_ticket, response.json())

    def test_get_tickets_with_concert_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket = response.json()

        other_concert = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': other_concert,
        })
        self.assertEqual(201, response.status_code)
        other_ticket = response.json()

        response = requests.get(self.host() + '/tickets?concert_id=' + concert_id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)
        self.assertIn(ticket, response.json())
        self.assertNotIn(other_ticket, response.json())

    def test_get_tickets_with_user_id_and_concert_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']

        response = requests.get(self.host() + '/tickets' + '?user_id=' + self.user_id + '&concert_id=' + concert_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertDictSubset({
            'user': {
                'id': self.user_id,
                'url': self.host() + '/users/' + self.user_id,
            },
            'concert': {
                'id': concert_id,
                'url': self.host() + '/concerts/' + concert_id,
            },
            'print_status': 'NOT_PRINTED',
        }, response.json()[0])

    def test_printing_missing_ticket(self):
        response = requests.post(self.host() + '/tickets/invalid_ticket_id/print')
        self.assertEqual(404, response.status_code)

    def test_printing_ticket(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']
        self.assertDictSubset({
            'print_status': 'NOT_PRINTED'
        }, response.json())

        response = requests.post(self.host() + '/tickets/' + ticket_id + '/print')
        self.assertEqual(202, response.status_code)

        response = requests.get(self.host() + '/tickets/' + ticket_id)
        self.assertEqual(200, response.status_code)

        status = response.json()['print_status']
        self.assertIn(status, ['PRINTED', 'PENDING'])

    def test_printing_ticket_wait(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
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

        # todo(eh): fix this to be proper time test
        # timeout after 3 minutes
        for i in range(0, 180):
            response = requests.get(self.host() + '/tickets/' + ticket_id)
            self.assertEqual(200, response.status_code)
            status = response.json()['print_status']
            if status == 'PRINTED':
                break
            time.sleep(1)

        status = response.json()['print_status']
        self.assertEqual('PRINTED', status)

        response = requests.get(self.host() + '/tickets/' + ticket_id + '/print')
        self.assertEqual(200, response.status_code)
        self.assertEqual('image/svg+xml', response.headers['Content-Type'])

        tree = ElementTree.fromstring(response.content)
        desc = tree.find('{http://www.w3.org/2000/svg}desc')
        self.assertIsNotNone(desc)
        self.assertEqual(ticket_id, desc.text)

    def test_ticket_getting_empty_print(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        ticket_id = response.json()['id']
        self.assertDictSubset({
            'print_status': 'NOT_PRINTED'
        }, response.json())

        response = requests.get(self.host() + '/tickets/' + ticket_id + '/print')
        self.assertEqual(404, response.status_code)

    def test_create_ticket_with_unexist_user_id(self):
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': '00000000-0020-0000-0000-000000000012',
            'concert_id': concert_id,
        })
        self.assertEqual(400, response.status_code)

    def test_check_returned_keys(self):
        """
        the returned structure should be like
{
    "id": "a4c5211f-2402-4de9-9664-b9e78454da35",
    "concert": {
        "id": "786d3bb4-a858-49ba-8803-15ffa2ec3678",
        "url": "http://tickets.api.ticketoverflow.com/api/v1/concerts/786d3bb4-a858-49ba-8803-15ffa2ec3678"
    },
    "user": {
        "id": "e571964f-f2b7-4200-9fb0-2af749092fa1",
        "url": "http://tickets.api.ticketoverflow.com/api/v1/users/e571964f-f2b7-4200-9fb0-2af749092fa1"
    },
    "print_status": "NOT_PRINTED"
}
        no extra keys should be returned
        :return:
        """

        # create a ticket
        concert_id = self.createConcert()
        response = requests.post(self.host() + '/tickets', json={
            'user_id': self.user_id,
            'concert_id': concert_id,
        })
        self.assertEqual(201, response.status_code)
        # check the returned keys of response.json()
        self.assertEqual(4, len(response.json()))
        ticket_id = response.json()['id']

        # get the ticket
        response = requests.get(self.host() + '/tickets/' + ticket_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response.json()))
        self.assertIn('id', response.json())
        self.assertIn('concert', response.json())
        self.assertIn('user', response.json())
        self.assertIn('print_status', response.json())



