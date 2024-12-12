from django.shortcuts import render
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Doctor, Appointment
from rest_framework import status
from .serializers import ClientSerializer, DoctorSerializer, AppointmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class LoginView(ObtainAuthToken):
    """
    - Description: Provides an endpoint for users to log in and receive an authentication token.
    - Methods:
            POST:
                - Validates user credentials.
                - Returns an authentication token and the user ID.
    - Response: {'token': <Token>, 'user_id': <User ID>}. 
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })

class UserView(APIView):
    """ 
    - Description: Base class for user management (shared between doctors and patients).
    - Helper Methods:
        - _validate_user: Checks if a username already exists.
        - _create_user: Creates a new user based on the provided credentials.
    Extended by: DoctorView, ClientView.
    """
    
    def _validate_user(self, username):
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists"
        return errors
    
    def _create_user(self, request):
        username = request.data.get("username").lower()
        password = request.data.get("password")
        first_name = request.data.get("firstname") 
        last_name = request.data.get("lastname")  
        errors = self._validate_user(username)
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        return user
class DoctorView(UserView):
    """
    - Description: Manages doctors (CRUD operations).
    - Methods:
        - DELETE:
            - Deletes a doctor and the associated user based on the provided ID.
            - Response: {"deleted User": <User's First Name>}.
        GET:
            - Retrieves information for a specific doctor or a list of all doctors.
            - Parameters: pk (optional, doctor ID).
            - Response: JSON data of the doctor or doctors.
        POST:
            - Creates a new user and doctor.
            - Response: {'user_id': <User ID>, 'email': <Email>}.
    - Helper Methods:
        - _create_doctor: Creates a doctor and saves it in the database.
        """
    def delete(self, request):
        x = request.data.get("id")
        user = User.objects.get(id=x)
        doctor = Doctor.objects.get(user_id=x)
        user.delete()
        doctor.delete()
        return Response({
            "deleted User": user.first_name
        }, status=status.HTTP_200_OK)
    
    def get(self, request, pk=None, format=None):
        
        if pk:
            doctor = get_object_or_404(Doctor, id=pk)
            serializer = DoctorSerializer(doctor)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)    
        return Response(serializer.data)
    
        
    def post(self, request, *args, **kwargs):
        user = self._create_user(request)
    
        if isinstance(user, Response):
            return user
    
        self._create_doctor(user, request)
    
        return Response(
            {
                'user_id': user.pk,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )
            
    
    def _create_doctor(self, user, request):
        title = request.data.get("title")
        speciality = request.data.get("speciality")  
        doctor = Doctor.objects.create(first_name = user.first_name, last_name = user.last_name, title = title, speciality = speciality,  user_id=user)
        doctor.save()
        return Response({
            'firstname': doctor.first_name,
            'lastname': doctor.last_name,
            'title': doctor.title,
            'speciality': doctor.speciality,
            'user_id': doctor.user_id
        })
    
    """ 
    - Description: Manages patients (CRUD operations).
    - Methods:
        - DELETE:
            - Deletes a patient and the associated user based on the provided ID.
            - Response: {"deleted User": <User's First Name>}.
        - GET:
            - Retrieves information for a specific patient or a list of all patients.
            - Parameters: pk (optional, patient ID).
            - Response: JSON data of the patient or patients.
        - POST:
            - Creates a new user and patient.
            - Response: {'user_id': <User ID>, 'email': <Email>}.
    - Helper Methods:
        - _create_client: Creates a patient and saves it in the database.
    """
class ClientView(UserView):
    
    def delete(self, request):
        x = request.data.get("id")
        user = User.objects.get(id=x)
        client = Client.objects.get(user_id=x)
        user.delete()
        client.delete()
        return Response({
            "deleted User": user.first_name
        }, status=status.HTTP_200_OK)
        
    
    def get(self, request, pk=None, format=None):
        
        if pk:
            client = get_object_or_404(Client, id=pk)
            serializer = ClientSerializer(client)
        else:
            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
 
    
        
    
    def post(self, request, *args, **kwargs):
        user = self._create_user(request) 
        
        if isinstance(user, Response):
            return user
            
        self._create_client(user)   
        return Response(
            {
                'user_id': user.pk,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )
        
    def _create_client(self, user): 
        client = Client.objects.create(first_name = user.first_name, last_name = user.last_name, user_id=user)
        client.save()
        return Response({
            'firstname': client.first_name,
            'lastname': client.last_name,
            'user_id': client.user_id
        })
   
   
    """
   - Description: Manages appointments (CRUD operations).
    - Authentication:
        - Requires token authentication.
        - Users must be authenticated.
    - Methods:
        - DELETE:
            - Deletes an appointment based on the provided ID.
            - Response: {"appointment deleted"}.
        - GET:
            - Retrieves information for a specific appointment or a list of all appointments for the authenticated user.
            - Parameters: pk (optional, appointment ID).
            - Response: JSON data of the appointment or appointments.
        - POST:
            - Creates a new appointment between a doctor and a patient.
            - Response: JSON data of the created appointment.
    """ 
class AppointmentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        x = request.data.get("id")
        appointment = Appointment.objects.get(id=x)
        appointment.delete()
        return Response({
            "appointment deleted"
        }, status=status.HTTP_200_OK)
    
    def get(self, request, pk=None, format=None):
        user = request.user.pk
        if pk:
            appointment = get_object_or_404(Appointment, id=pk)
            serializer = AppointmentSerializer(appointment)
        else:
            appointments = Appointment.objects.filter(user_id=user)
            serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        d = request.data.get("doctor_id")
        c = request.data.get("client_id")
        doctor = Doctor.objects.get(id=d)
        client = Client.objects.get(id=c)
        title = request.data.get("title")
        description = request.data.get("description")
        date = request.data.get("date")
        appointment = Appointment.objects.create(doctor_id=doctor, client_id = client, title = title, description = description, date = date, user_id=user)
        appointment.save()
        return Response({
            'doctor_id': appointment.doctor_id.id,
            'client_id': appointment.client_id.id,
            'title': appointment.title,
            'description': appointment.description,
            'date': appointment.date,
            'user_id': appointment.user_id.id,
        })
