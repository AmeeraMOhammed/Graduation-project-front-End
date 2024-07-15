# serializer.py

from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import CustomUser,Patient
from django.core.validators import MinLengthValidator  # Import the validator
from datetime import date
# from .models import ImageModel
from .eyebrows import calculate_distances
from .mouth import calculate_distances_mouth
from .eye_area import calculate_and_draw_eye_areas
import cv2
from io import BytesIO
from .eye_dl import predict_image_eye
from .eyebrow_dl import predict_image_eyebrow
from .mouth_dl import predict_image_mouth



class CustomLoginSerializer(LoginSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')



class CustomRegisterSerializer(RegisterSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        # self.fields.pop('password')
        self.fields.pop('password2')


    first_name  = serializers.CharField(required=True,max_length=30)
    last_name = serializers.CharField(required=True,max_length=30)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=False, min_length=8)  
    birthdate = serializers.DateField(input_formats=['%d/%m/%Y'])
    # birthdate = serializers.DateField(required=False)
    title = serializers.CharField(required=True, max_length=100)
    gender = serializers.CharField(required=True, max_length=100)
    mobileNumber = serializers.CharField(required=True, max_length=100)
    # image_url = serializers.ImageField(required=False)
    original_image_eyebrows = serializers.ImageField(required=False)
    original_image_mouth = serializers.ImageField(required=False)
    original_image_eye = serializers.ImageField(required=False)
    working_days = serializers.JSONField(required=False)



    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['birthdate'] = self.validated_data.get('birthdate', '')
        data_dict['title'] = self.validated_data.get('title', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['mobileNumber'] = self.validated_data.get('mobileNumber', '')
        data_dict['original_image_eyebrows'] = self.validated_data.get('original_image_eyebrows', '')
        data_dict['filtered_image_eyebrows'] = self.validated_data.get('filtered_image_eyebrows', '')
        data_dict['original_image_mouth'] = self.validated_data.get('original_image_mouth', '')
        data_dict['filtered_image_mouth'] = self.validated_data.get('filtered_image_mouth', '')
        data_dict['original_image_eye'] = self.validated_data.get('original_image_eye', '')
        data_dict['filtered_image_eye'] = self.validated_data.get('filtered_image_eye', '')
        data_dict['email'] = self.validated_data.get('email', '')
        data_dict['password1'] = self.validated_data.get('password1', '')
        data_dict['right_eyebrow_distance'] = self.validated_data.get('right_eyebrow_distance', '')
        data_dict['left_eyebrow_distance'] = self.validated_data.get('left_eyebrow_distance', '')
        data_dict['right_mouth_distance'] = self.validated_data.get('right_mouth_distance', '')
        data_dict['left_mouth_distance'] = self.validated_data.get('left_mouth_distance', '')
        data_dict['right_eye_area'] = self.validated_data.get('right_eye_area', '')
        data_dict['left_eye_area'] = self.validated_data.get('left_eye_area', '')
        data_dict['abs_difference_eye'] = self.validated_data.get('abs_difference_eye', '')
        data_dict['abs_difference_eyebrows'] = self.validated_data.get('abs_difference_eyebrows', '')
        data_dict['abs_difference_mouth'] = self.validated_data.get('abs_difference_mouth', '')
        data_dict['working_days'] = self.validated_data.get('working_days', '')
        data_dict['eyebrow_classification'] = self.validated_data.get('eyebrow_classification', '')
        data_dict['mouth_classification'] = self.validated_data.get('mouth_classification', '')
        data_dict['eye_classification'] = self.validated_data.get('eye_classification', '')

        return data_dict
    
    
    def validate(self, data):
        title = data.get('title')
        original_image_eyebrows = data.get('original_image_eyebrows')
        original_image_mouth = data.get('original_image_mouth')
        original_image_eye = data.get('original_image_eye')

        if title == 'Patient' and not original_image_eyebrows and not original_image_mouth and not original_image_eye:
            raise serializers.ValidationError("Image is required for patients.")
        
        return data
    
    def save(self, request):
        self.is_valid(raise_exception=True)
        user = super().save(request)
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    original_image_eyebrows = serializers.ImageField(required=False)
    filtered_image_eyebrows = serializers.ImageField(required=False)
    original_image_mouth = serializers.ImageField(required=False)
    filtered_image_mouth = serializers.ImageField(required=False)
    original_image_eye = serializers.ImageField(required=False)
    filtered_image_eye = serializers.ImageField(required=False)
    doctor = serializers.SerializerMethodField()
    # patients = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    right_eyebrow_distance = serializers.FloatField(required=False)
    left_eyebrow_distance = serializers.FloatField(required=False)
    right_mouth_distance = serializers.FloatField(required=False)
    left_mouth_distance = serializers.FloatField(required=False)
    right_eye_area = serializers.FloatField(required=False)
    left_eye_area = serializers.FloatField(required=False)
    abs_difference_eyebrows = serializers.FloatField(required=False)
    abs_difference_mouth = serializers.FloatField(required=False)
    abs_difference_eye = serializers.FloatField(required=False)
    working_days = serializers.JSONField(required=False)
    eyebrow_classification = serializers.CharField(required=False)
    mouth_classification = serializers.CharField(required=False)
    eye_classification = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'first_name', 'last_name', 'email', 'birthdate', 'title', 'gender', 
            'mobileNumber', 'original_image_eyebrows', 'filtered_image_eyebrows', 
            'original_image_mouth', 'filtered_image_mouth', 'original_image_eye', 
            'filtered_image_eye', 'doctor', 'age', 'right_eyebrow_distance','left_eyebrow_distance',
            'right_mouth_distance','left_mouth_distance','right_eye_area','left_eye_area','abs_difference_eyebrows'
            ,'abs_difference_eye','abs_difference_mouth', 'working_days','eyebrow_classification','mouth_classification'
            ,'eye_classification'
        )

    def get_age(self, obj):
        today = date.today()
        if obj.birthdate:
            age = today.year - obj.birthdate.year - ((today.month, today.day) < (obj.birthdate.month, obj.birthdate.day))
            return age
        return None

    def get_doctor(self, obj):
        if obj.title.lower() == 'patient':
            if hasattr(obj, 'patient') and obj.patient.doctor:
                return {
                    'id': obj.patient.doctor.id,
                    'username': obj.patient.doctor.username,
                    'full_name': f"{obj.patient.doctor.first_name} {obj.patient.doctor.last_name}",
                    'email': obj.patient.doctor.email,
                    'mobileNumber' : obj.patient.doctor.mobileNumber,
                    'working_days' : obj.patient.doctor.working_days
                }
            return "None"
        return None


    
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[MinLengthValidator(1)], required=False)
    last_name = serializers.CharField(validators=[MinLengthValidator(1)], required=False)
    mobileNumber = serializers.CharField(validators=[MinLengthValidator(1)], required=False)
    email = serializers.CharField(validators=[MinLengthValidator(1)], required=False)
    # password1 = serializers.CharField(validators=[MinLengthValidator(1)], required=False)
    original_image_eyebrows = serializers.ImageField(validators=[MinLengthValidator(1)], required=False)
    original_image_mouth = serializers.ImageField(validators=[MinLengthValidator(1)], required=False)
    original_image_eye = serializers.ImageField(validators=[MinLengthValidator(1)], required=False)
    working_days = serializers.JSONField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobileNumber', 'email', 'original_image_eyebrows', 'original_image_eye', 'original_image_mouth','working_days']

    def update(self, instance, validated_data):
        # Append current values to previous lists if new images are uploaded
        if 'original_image_eyebrows' in validated_data:
            if instance.right_eyebrow_distance is not None:
                instance.previous_right_eyebrow_distance = (instance.previous_right_eyebrow_distance or []) + [instance.right_eyebrow_distance]
            if instance.left_eyebrow_distance is not None:
                instance.previous_left_eyebrow_distance = (instance.previous_left_eyebrow_distance or []) + [instance.left_eyebrow_distance]
            if instance.abs_difference_eyebrows is not None:
                instance.previous_abs_difference_eyebrows = (instance.previous_abs_difference_eyebrows or []) + [instance.abs_difference_eyebrows]

        if 'original_image_mouth' in validated_data:
            if instance.right_mouth_distance is not None:
                instance.previous_right_mouth_distance = (instance.previous_right_mouth_distance or []) + [instance.right_mouth_distance]
            if instance.left_mouth_distance is not None:
                instance.previous_left_mouth_distance = (instance.previous_left_mouth_distance or []) + [instance.left_mouth_distance]
            if instance.abs_difference_mouth is not None:
                instance.previous_abs_difference_mouth = (instance.previous_abs_difference_mouth or []) + [instance.abs_difference_mouth]

        if 'original_image_eye' in validated_data:
            if instance.right_eye_area is not None:
                instance.previous_right_eye_area = (instance.previous_right_eye_area or []) + [instance.right_eye_area]
            if instance.left_eye_area is not None:
                instance.previous_left_eye_area = (instance.previous_left_eye_area or []) + [instance.left_eye_area]
            if instance.abs_difference_eye is not None:
                instance.previous_abs_difference_eye = (instance.previous_abs_difference_eye or []) + [instance.abs_difference_eye]

        # Update the instance with new values
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance to trigger the processing of images and saving of distances
        instance.save()

        # If the original image for eyebrows has been uploaded, process and save the filtered image and distances
        if 'original_image_eyebrows' in validated_data:
            # Perform image processing for eyebrows
            filtered_image_eyebrows, right_eyebrow_distance, left_eyebrow_distance, abs_difference_eyebrows = calculate_distances(instance.original_image_eyebrows)
            _, buffer = cv2.imencode(".jpg", filtered_image_eyebrows)
            filtered_image_eyebrows_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            instance.filtered_image_eyebrows.save('filtered_image_eyebrows.jpg', BytesIO(filtered_image_eyebrows_bytes))
            instance.right_eyebrow_distance = right_eyebrow_distance
            instance.left_eyebrow_distance = left_eyebrow_distance
            instance.abs_difference_eyebrows = abs_difference_eyebrows
            instance.eyebrow_classification = predict_image_eyebrow(instance.original_image_eyebrows)

        # If the original image for mouth has been uploaded, process and save the filtered image and distances
        if 'original_image_mouth' in validated_data:
            # Perform image processing for mouth
            filtered_image_mouth, right_mouth_distance, left_mouth_distance, abs_difference_mouth = calculate_distances_mouth(instance.original_image_mouth)
            _, buffer = cv2.imencode(".jpg", filtered_image_mouth)
            filtered_image_mouth_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            instance.filtered_image_mouth.save('filtered_image_mouth.jpg', BytesIO(filtered_image_mouth_bytes))
            instance.right_mouth_distance = right_mouth_distance
            instance.left_mouth_distance = left_mouth_distance
            instance.abs_difference_mouth = abs_difference_mouth
            instance.mouth_classification = predict_image_mouth(instance.original_image_mouth)

        # If the original image for eyes has been uploaded, process and save the filtered image and areas
        if 'original_image_eye' in validated_data:
            # Perform image processing for eyes
            filtered_image_eye, right_eye_area, left_eye_area, abs_difference_eye = calculate_and_draw_eye_areas(instance.original_image_eye)
            _, buffer = cv2.imencode(".jpg", filtered_image_eye)
            filtered_image_eye_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            instance.filtered_image_eye.save('filtered_image_eye.jpg', BytesIO(filtered_image_eye_bytes))
            instance.right_eye_area = right_eye_area
            instance.left_eye_area = left_eye_area
            instance.abs_difference_eye = abs_difference_eye
            instance.eye_classification = predict_image_eye(instance.original_image_eye)

        # Save the instance again to update all fields
        instance.save()
        return instance
class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'email', 'mobileNumber','working_days')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class AssignDoctorSerializer(serializers.Serializer):
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(title='doctor'))



class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    original_image_eyebrows = serializers.SerializerMethodField()
    filtered_image_eyebrows = serializers.SerializerMethodField()
    original_image_mouth = serializers.SerializerMethodField()
    filtered_image_mouth = serializers.SerializerMethodField()
    original_image_eye = serializers.SerializerMethodField()
    filtered_image_eye = serializers.SerializerMethodField()
    right_eyebrow_distance = serializers.FloatField(required=False)
    left_eyebrow_distance = serializers.FloatField(required=False)
    right_mouth_distance = serializers.FloatField(required=False)
    left_mouth_distance = serializers.FloatField(required=False)
    right_eye_area = serializers.FloatField(required=False)
    left_eye_area = serializers.FloatField(required=False)
    abs_difference_eyebrows = serializers.FloatField(required=False)
    abs_difference_mouth = serializers.FloatField(required=False)
    abs_difference_eye = serializers.FloatField(required=False)
    eyebrow_classification = serializers.CharField(required=False)
    mouth_classification = serializers.CharField(required=False)
    eye_classification = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'birthdate', 'age', 'gender',
            'mobileNumber', 'original_image_eyebrows', 'filtered_image_eyebrows',
            'original_image_mouth', 'filtered_image_mouth', 'original_image_eye',
            'filtered_image_eye', 'right_eyebrow_distance', 'left_eyebrow_distance',
            'right_mouth_distance', 'left_mouth_distance', 'right_eye_area', 'left_eye_area',
            'abs_difference_eye', 'abs_difference_mouth', 'abs_difference_eyebrows','eyebrow_classification',
            'mouth_classification'  ,'eye_classification'
        ]

    def get_age(self, obj):
        today = date.today()
        if obj.birthdate:
            age = today.year - obj.birthdate.year - ((today.month, today.day) < (obj.birthdate.month, obj.birthdate.day))
            return age
        return None

    def get_image_url(self, obj, field_name):
        if field_name:
            url = getattr(obj, field_name).url
            return self.context['request'].build_absolute_uri(url)
        return None

    def get_original_image_eyebrows(self, obj):
        return self.get_image_url(obj, 'original_image_eyebrows')

    def get_filtered_image_eyebrows(self, obj):
        return self.get_image_url(obj, 'filtered_image_eyebrows')

    def get_original_image_mouth(self, obj):
        return self.get_image_url(obj, 'original_image_mouth')

    def get_filtered_image_mouth(self, obj):
        return self.get_image_url(obj, 'filtered_image_mouth')

    def get_original_image_eye(self, obj):
        return self.get_image_url(obj, 'original_image_eye')

    def get_filtered_image_eye(self, obj):
        return self.get_image_url(obj, 'filtered_image_eye')

class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Use the CustomUserSerializer for the 'user' field
    date_selected = serializers.DateField()  # Ensure this field is included

    class Meta:
        model = Patient
        fields = '__all__'  # Include all fields from the Patient model



# class CustomUserSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name',
#                    'right_eyebrow_distance','left_eyebrow_distance',
#                     'right_mouth_distance','left_mouth_distance','right_eye_area',
#                     'left_eye_area','abs_difference_eye','abs_difference_mouth','abs_difference_eyebrows']  # Include all fields from the CustomUser model





















class CustomUserProgressSerializer(serializers.ModelSerializer):
    right_eyebrow_diff = serializers.SerializerMethodField()
    left_eyebrow_diff = serializers.SerializerMethodField()
    right_mouth_diff = serializers.SerializerMethodField()
    left_mouth_diff = serializers.SerializerMethodField()
    right_eye_diff = serializers.SerializerMethodField()
    left_eye_diff = serializers.SerializerMethodField()
    diff_abs_difference_mouth = serializers.SerializerMethodField()
    diff_abs_difference_eyebrows = serializers.SerializerMethodField()
    diff_abs_difference_eye = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'right_eyebrow_distance', 'left_eyebrow_distance', 'previous_right_eyebrow_distance', 'previous_left_eyebrow_distance', 'right_eyebrow_diff', 'left_eyebrow_diff',
            'diff_abs_difference_eyebrows', 'abs_difference_eyebrows', 'previous_abs_difference_eyebrows',
            'right_mouth_distance', 'left_mouth_distance', 'previous_right_mouth_distance', 'previous_left_mouth_distance', 'right_mouth_diff', 'left_mouth_diff',
            'diff_abs_difference_mouth', 'abs_difference_mouth', 'previous_abs_difference_mouth',
            'right_eye_area', 'left_eye_area', 'previous_right_eye_area', 'previous_left_eye_area', 'right_eye_diff', 'left_eye_diff', 'diff_abs_difference_eye',
            'abs_difference_eye', 'previous_abs_difference_eye',
        ]

    def subtract_sequential(self, previous_values):
        if previous_values is None:
            return None
        
        # Reverse the list and compute differences
        # reversed_previous_values = previous_values[::-1]  # Reverse the list
        differences = [previous_values[i] - previous_values[i+1]  for i in range(len(previous_values) - 1)]
        return differences

    def get_right_eyebrow_diff(self, obj):
        previous_values = obj.previous_right_eyebrow_distance
        return self.subtract_sequential( previous_values)

    def get_left_eyebrow_diff(self, obj):
        previous_values = obj.previous_left_eyebrow_distance
        return self.subtract_sequential(previous_values)

    def get_diff_abs_difference_eyebrows(self, obj):
        previous_values = obj.previous_abs_difference_eyebrows
        return self.subtract_sequential( previous_values)

    def get_right_mouth_diff(self, obj):
        previous_values = obj.previous_right_mouth_distance
        return self.subtract_sequential( previous_values)

    def get_left_mouth_diff(self, obj):
        previous_values = obj.previous_left_mouth_distance
        return self.subtract_sequential( previous_values)

    def get_diff_abs_difference_mouth(self, obj):
        previous_values = obj.previous_abs_difference_mouth
        return self.subtract_sequential( previous_values)

    def get_right_eye_diff(self, obj):
        previous_values = obj.previous_right_eye_area
        return self.subtract_sequential( previous_values)

    def get_left_eye_diff(self, obj):
        previous_values = obj.previous_left_eye_area
        return self.subtract_sequential(previous_values)

    def get_diff_abs_difference_eye(self, obj):
        previous_values = obj.previous_abs_difference_eye
        return self.subtract_sequential( previous_values)

class ProgressSerializer(serializers.ModelSerializer):
    user = CustomUserProgressSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

class ProgressSerializer1(serializers.ModelSerializer):
    # user = CustomUserProgressSerializer()

    class Meta:
        model = CustomUser
        fields = '__all__'

