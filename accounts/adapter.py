# adapter.py

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.firstName = data.get('firstName')
        user.email = data.get('email')
        user.password1 = data.get('password1')
        user.secondName = data.get('secondName')
        user.birthdate = data.get('birthdate')
        user.title = data.get('title')
        user.gender = data.get('gender')
        user.mobileNumber = data.get('mobileNumber')
        user.original_image_eyebrows = data.get('original_image_eyebrows')
        user.filtered_image_eyebrows = data.get('filtered_image_eyebrows')
        user.original_image_mouth= data.get('original_image_mouth')
        user.filtered_image_mouth = data.get('filtered_image_mouth')
        user.original_image_eye = data.get('original_image_eye')
        user.filtered_image_eye = data.get('filtered_image_eye')
        user.working_days = data.get('working_days')
        # user.right_eyebrow_distance = data.get('right_eyebrow_distance')
        # user.left_eyebrow_distance = data.get('left_eyebrow_distance')
        # user.right_mouth_distance = data.get('right_mouth_distance')
        # user.left_mouth_distance = data.get('left_mouth_distance')
        # user.abs_difference_mouth = data.get('abs_difference_mouth')
        # user.right_eye_area = data.get('right_eye_area')
        # user.left_eye_area = data.get('left_eye_area')
        # user.abs_difference_eye = data.get('abs_difference_eye')

        user.save()
        return user