from django.test import TestCase


class ViewTest(TestCase):
    def test_home_page(self):
        print('******************test_home_page()**********************')
        # send GET request.
        response = self.client.get('/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_manager/index.html')


    def test_root_not_correct(self):
        print('******************test_root_not_correct()**********************')
        login_account_test_data = {'username': 'admin', 'password': 'qqqqqq'}
        response = self.client.post(path='/admin/login/', data=login_account_test_data)
        print('Response status code : ' + str(response.status_code))
        # print('Response content : ' + str(response.content))
        self.assertEqual(response.status_code, 200)
        # if the provided string exist in the response content html, then pass.
        self.assertNotIn(b'Users', response.content)

    def test_login_success(self):
        print('******************test_root_success()**********************')
        login_account_test_data = {'username': 'root', 'password': 'root'}
        response = self.client.post(path='/admin/login/', data=login_account_test_data)
        print('Response status code : ' + str(response.status_code))
        self.assertNotIn(b'User name or password is not correct', response.content)
