# view.py
from rest_framework.response import Response
from .serializers import CustomRegisterSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomUserDetailsSerializer
from .eyebrows import calculate_distances
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, CustomLoginSerializer, CustomUserDetailsSerializer, CustomUserUpdateSerializer
from .serializers import DoctorSerializer,AssignDoctorSerializer
from .models import CustomUser
from .models import Patient, CustomUser
from .serializers import PatientSerializer,ProgressSerializer,ProgressSerializer1


class CustomUserDetailView(generics.RetrieveAPIView):
    serializer_class = CustomUserDetailsSerializer
    # serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


    
class CustomUserUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Ensure parsers are set to handle file uploads

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        instance = self.get_object()
        # Call the serializer's save method to update the user instance
        serializer.save()
        # Trigger image processing by saving the instance
        instance.save()


class MyModelViewSet(viewsets.ModelViewSet):
    # queryset = CustomUser.objects.order_by('-creation_date')
    serializer_class = CustomRegisterSerializer

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        # Original response
        response = super().get_response()
        # Add custom data to response
        custom_data = {
            'title': self.user.title,
            'gender': self.user.gender,

        }
        response.data.update(custom_data)
        return response
    

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        # Original response data
        original_data = super().get_response_data(user)
        # Add custom data
        custom_data = {
            'title': user.title,
            'gender': user.gender,
        }
        original_data.update(custom_data)
        return original_data
    

class DoctorPatientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Ensure the user is a doctor
        if request.user.title.lower() != 'doctor':
            return Response({"detail": "Only doctors can view this information."}, status=403)

        # Get the patients assigned to the doctor
        patients = Patient.objects.filter(doctor=request.user)
        serializer = PatientSerializer(patients, many=True, context={'request': request})
        return Response(serializer.data)

        
from django.utils import timezone

class SelectDoctorView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        doctors = CustomUser.objects.filter(title='doctor')
        print(f"Doctors found: {doctors.count()}")

        if not doctors.exists():
            return Response({'error': 'No doctors found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AssignDoctorSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor_id']
            patient, created = Patient.objects.get_or_create(user=request.user)
            patient.doctor = doctor
            patient.date_selected = timezone.now()  # Set the date_selected to current time
            patient.save()
            return Response({'message': 'Doctor successfully assigned to patient'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# class ProgressView(generics.ListAPIView):
#     serializer_class = ProgressSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.title.lower() == 'doctor':
#             # Return progress data for all patients assigned to this doctor
#             return Patient.objects.filter(doctor=user)
#         elif user.title.lower() == 'patient':
#             # Return progress data for the logged-in patient
#             return Patient.objects.filter(user=user)
#         return Patient.objects.none() 


class ProgressView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user

        # Check if the user is a doctor or patient based on title
        if user.title.lower() == 'doctor':
            # Return progress data for all patients assigned to this doctor
            patients = Patient.objects.filter(doctor=user)
            serializer = ProgressSerializer(patients, many=True)
        elif user.title.lower() == 'patient':
            try:
                # Try to retrieve patient data for the logged-in patient
                patient = Patient.objects.get(user=user)
                serializer = ProgressSerializer(patient)
            except Patient.DoesNotExist:
                # If patient data doesn't exist, return ProgressSerializer1 for the user
                serializer = ProgressSerializer1(user)

        return Response(serializer.data, status=status.HTTP_200_OK)