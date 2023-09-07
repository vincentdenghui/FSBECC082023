import requests
import unittest




class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        ...
    def tearDown(self):
        ...

    def get_url(self,route):
        return f'http://localhost:8000{route}'

    # FRi1. can visit the home page
    def test_can_visit_the_default_home_page(self):
        response = requests.get(self.get_url('/'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('lenders' in response.json())

    # FR1. Create a new Lender

    # FR2. List all Lenders (five per page)

    # FR1. List active lenders

    # FR3. Get a specific Lender

    # FR4. Update a specific Lender

    # FR5. Delete a specific Lender

    # FR6. Bulk upload Lenders in CSV format

    # FR7. Download Lenders in CSV format





if __name__ == '__main__':
    unittest.main()






