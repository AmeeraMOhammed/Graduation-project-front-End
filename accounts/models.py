# models.py
from django.db import models
from io import BytesIO
from django.contrib.auth.models import AbstractUser
from .eyebrows import calculate_distances
from .mouth import calculate_distances_mouth
from .eye_area import calculate_and_draw_eye_areas
import cv2
from .eye_dl import predict_image_eye
from .eyebrow_dl import predict_image_eyebrow
from .mouth_dl import predict_image_mouth


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class CustomUser(AbstractUser): 

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=10, choices=[('doctor', 'doctor'), ('patient', 'patient')])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    mobileNumber = models.CharField(max_length=15, null=True, blank=True)

    original_image_eyebrows = models.ImageField(upload_to=upload_to, blank=True, null=True)
    filtered_image_eyebrows = models.ImageField(upload_to=upload_to, blank=True, null=True)
    right_eyebrow_distance = models.FloatField(null=True, blank=True)
    left_eyebrow_distance = models.FloatField(null=True, blank=True)
    abs_difference_eyebrows = models.FloatField(null=True, blank=True)
    previous_right_eyebrow_distance = models.JSONField(default=list, blank=True)
    previous_left_eyebrow_distance = models.JSONField(default=list, blank=True)
    previous_abs_difference_eyebrows = models.JSONField(default=list, blank=True)
    eyebrow_classification = models.CharField(max_length=50, blank=True, null=True)

    original_image_mouth = models.ImageField(upload_to=upload_to, blank=True, null=True)
    filtered_image_mouth = models.ImageField(upload_to=upload_to, blank=True, null=True)
    right_mouth_distance = models.FloatField(null=True, blank=True)
    left_mouth_distance = models.FloatField(null=True, blank=True)
    abs_difference_mouth = models.FloatField(null=True, blank=True)
    previous_right_mouth_distance = models.JSONField(default=list, blank=True)
    previous_left_mouth_distance = models.JSONField(default=list, blank=True)
    previous_abs_difference_mouth = models.JSONField(default=list, blank=True)
    mouth_classification = models.CharField(max_length=50, blank=True, null=True)

    original_image_eye = models.ImageField(upload_to=upload_to, blank=True, null=True)
    filtered_image_eye = models.ImageField(upload_to=upload_to, blank=True, null=True)
    right_eye_area = models.FloatField(null=True, blank=True)
    left_eye_area = models.FloatField(null=True, blank=True)
    abs_difference_eye = models.FloatField(null=True, blank=True)
    previous_right_eye_area = models.JSONField(default=list, blank=True)
    previous_left_eye_area = models.JSONField(default=list, blank=True)
    previous_abs_difference_eye = models.JSONField(default=list, blank=True)
    eye_classification = models.CharField(max_length=50, blank=True, null=True)

    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=128)
    working_days = models.JSONField(default=list, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the original image for eyebrows has been uploaded and is not yet processed
        if self.original_image_eyebrows and not self.filtered_image_eyebrows:
            # Perform image processing for eyebrows
            filtered_image_eyebrows,right_eyebrow_distance,  left_eyebrow_distance, abs_difference_eyebrows = calculate_distances(self.original_image_eyebrows)
            _, buffer = cv2.imencode(".jpg", filtered_image_eyebrows)
            filtered_image_eyebrows_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            self.filtered_image_eyebrows.save('filtered_image_eyebrows.jpg', BytesIO(filtered_image_eyebrows_bytes))
            self.right_eyebrow_distance = right_eyebrow_distance
            self.left_eyebrow_distance = left_eyebrow_distance
            self.abs_difference_eyebrows = abs_difference_eyebrows
            self.eyebrow_classification = predict_image_eyebrow(self.original_image_eyebrows)

        # Check if the original image for mouth has been uploaded and is not yet processed
        if self.original_image_mouth and not self.filtered_image_mouth:
            # Perform image processing for mouth
            filtered_image_mouth, right_mouth_distance, left_mouth_distance , abs_difference_mouth = calculate_distances_mouth(self.original_image_mouth)
            _, buffer = cv2.imencode(".jpg", filtered_image_mouth)
            filtered_image_mouth_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            self.filtered_image_mouth.save('filtered_image_mouth.jpg', BytesIO(filtered_image_mouth_bytes))
            self.right_mouth_distance = right_mouth_distance
            self.left_mouth_distance = left_mouth_distance
            self.abs_difference_mouth = abs_difference_mouth
            self.mouth_classification = predict_image_mouth(self.original_image_mouth)

        # Check if the original image for mouth has been uploaded and is not yet processed
        if self.original_image_eye and not self.filtered_image_eye:
            # Perform image processing for mouth
            filtered_image_eye, right_eye_area, left_eye_area,  abs_difference_eye = calculate_and_draw_eye_areas(self.original_image_eye)
            _, buffer = cv2.imencode(".jpg", filtered_image_eye)
            filtered_image_eye_bytes = buffer.tobytes()
            # Save the filtered image bytes to the model instance
            self.filtered_image_eye.save('filtered_image_eye.jpg', BytesIO(filtered_image_eye_bytes))
            self.right_eye_area = right_eye_area
            self.left_eye_area = left_eye_area
            self.abs_difference_eye = abs_difference_eye
            self.eye_classification = predict_image_eye(self.original_image_eye)

        # Call the parent class save method after processing the images
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    date_selected = models.DateField(null=True, blank=True)  # Add this field if it doesn't exist
