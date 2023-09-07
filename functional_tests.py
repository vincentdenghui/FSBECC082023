import requests
import unittest
import os
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth
from rest_framework import status

load_dotenv(find_dotenv())

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.djang_user = os.environ['DJANGO_USER']
        self.djang_user_password = os.environ['DJANGO_USER_PASSWORD']
        self.basic_authentication_object = HTTPBasicAuth(self.djang_user, self.djang_user_password)
        self.test_users = []


        #user for readonly checks
        self.test_ro_lender_code = 'TRO'
        self.test_ro_lender_name = 'SampleName'

    def tearDown(self):
        ...#remove TRO user

    def get_url(self,route):
        return f'http://localhost:8000{route}'

    #FRi1. can visit the home page
    def test_can_visit_the_default_home_page(self):
        response = requests.get(self.get_url('/'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('lenders' in response.json())



    def test_user_can_create_lender_for_read_only_check(self):
        requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name':self.test_ro_lender_name,
                            'code': self.test_ro_lender_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': True})
        self.assertEqual(requests.get(self.get_url(f'/lenders/{self.test_ro_lender_code}')).json()['name'],
                         self.test_ro_lender_name)


    # FR1. Create a new Lender
    def test_user_can_create_lender(self):
        test_code = 'TGP'
        test_name = 'tgf7qh8o3y45'
        res = requests.post(self.get_url('/lenders/'),
                      auth=self.basic_authentication_object,
                      json={'name':test_name,
                            'code': test_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(requests.get(self.get_url(f'/lenders/{test_code}')).json()['name'],test_name)

    def test_user_can_get_lender(self):
        self.assertEqual(
            requests.get(
                self.get_url(f'/lenders/{self.test_ro_lender_code}'),
                auth=self.basic_authentication_object
            ).json()['name'],
            self.test_ro_lender_name
        )

    def test_visitors_cannot_create_lender(self):
        test_code = 'TGQ'
        test_name = 'tgf7qh8o3y46'
        res = requests.post(self.get_url('/lenders/'),
                      json={'name':test_name,
                            'code': test_code,
                            'upfront_commission_rate': 100,
                            'trial_commission_rate': 200,
                            'active': False})
        self.assertNotEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(requests.get(self.get_url(f'/lenders/{test_code}')).status_code,status.HTTP_404_NOT_FOUND)

    # FR2. List all Lenders (five per page)
    def test_user_can_see_pagination(self):
        #create 6 lenders
        for i in range(65,72):
            character = chr(i).upper()
            requests.post(self.get_url('/lenders/'),
                            auth=self.basic_authentication_object,
                            json={'name': f'pagination_test_{character}',
                                  'code': f'PT{character}',
                                  'upfront_commission_rate': 100,
                                  'trial_commission_rate': 200,
                                  'active': True})
        self.assertEqual(len(requests.get(self.get_url('/lenders/')).json()['results']), 5)
        self.assertNotEqual(len(requests.get(self.get_url('/lenders/?page=2')).json()['results']), 5)


        ...
    # FR1. List active lenders

    # FR3. Get a specific Lender

    # FR4. Update a specific Lender

    # FR5. Delete a specific Lender

    # FR6. Bulk upload Lenders in CSV format

    # FR7. Download Lenders in CSV format





if __name__ == '__main__':
    unittest.main()






