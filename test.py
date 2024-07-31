import json
import unittest
from unittest.mock import patch
from app import create_app, db, bcrypt


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        with open('config.json') as f:
            config = json.load(f)
        self.app.config.update(config)
        self.client = self.app.test_client()

    def test_get_register(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    @patch('app.bcrypt.generate_password_hash')
    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    @patch('app.send_registration_email')
    def test_register_post_success(self, mock_send_email, mock_add, mock_commit, mock_hash):
        mock_hash.return_value = 'hashed_password'

        with patch('app.RegisterForm') as mock_form:
            mock_form.return_value.validate_on_submit.return_value = True
            mock_form.return_value.firstName.data = 'khalil'
            mock_form.return_value.lastName.data = 'bouazizi'
            mock_form.return_value.email.data = 'khalilbouazizi@example.com'
            mock_form.return_value.telephone.data = '5555555'
            mock_form.return_value.password.data = 'test'

            response = self.client.post('/register', data={
                'firstName': 'khalil',
                'lastName': 'bouazizi',
                'email': 'khalilbouazizi@example.com',
                'telephone': '5555555',
                'password': 'test',
                'confirmpassword': 'test'
            })
            self.assertEqual(response.status_code, 302)
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_send_email.assert_called_once_with('khalilbouazizi@example.com')


class LogoutTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        with open('config.json') as f:
            config = json.load(f)
        self.app.config.update(config)
        self.client = self.app.test_client()

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_logout_post_success(self):
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
