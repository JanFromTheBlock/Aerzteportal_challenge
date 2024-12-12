from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from User.models import Doctor, Client


class DoctorTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.request_doctor = {'title': 'Dr. med', 'speciality': 'neurology'}
        self.doctor = Doctor.objects.create(first_name = 'Jess', last_name = 'Klaasen', title = 'Dr.', speciality = 'neurology',  user_id=self.user2)
        self.patient = Client.objects.create(first_name = 'Joachim', last_name = 'Löw', user_id=self.user2)
    
    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_wrong_data(self):
        url = reverse('login')
        data = {
            'username': 'testuser10',
            'password': 'testpassword10'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_doctor(self):
        url = reverse('doctor')
        data = {
            'username': 'Jens1234',
            'password': 'pw123456',
            'title': 'Dr. Dr.',
            'firstname': 'Jens',
            'lastname': 'Jenser',
            'speciality': 'internist'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_doctor_with_same_username(self):
        url = reverse('doctor')
        data = {
            'username': 'testuser',
            'password': 'pw123456',
            'title': 'Dr. Dr.',
            'firstname': 'Jens',
            'lastname': 'Jenser',
            'speciality': 'internist'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_doctors(self):
        url = reverse('doctor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_doctor(self):
        pk = self.doctor.id
        url = reverse('doctor-single', kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_doctor(self):
        url = reverse('doctor')
        data = {'id': 2}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class ClientTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.request_doctor = {'title': 'Dr. med', 'speciality': 'neurology'}
        self.doctor = Doctor.objects.create(first_name = 'Jess', last_name = 'Klaasen', title = 'Dr.', speciality = 'neurology',  user_id=self.user2)
        self.patient = Client.objects.create(first_name = 'Joachim', last_name = 'Löw', user_id=self.user2)
    
        
    def test_create_client(self):
        url = reverse('client')
        data = {
            'username': 'Jens12345',
            'password': 'pw123456',
            'firstname': 'Jens',
            'lastname': 'Jenser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_client_with_same_username(self):
        url = reverse('client')
        data = {
            'username': 'testuser',
            'password': 'pw123456',
            'firstname': 'Jens',
            'lastname': 'Jenser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_doctors(self):
        url = reverse('client')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_doctor(self):
        pk = self.patient.id
        url = reverse('client-single', kwargs={"pk": pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_client(self):
        url = reverse('client')
        data = {'id': 2}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        