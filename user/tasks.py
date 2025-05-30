from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email(email, uid, token):
    subject = 'Activate your Charity account'
    activation_link = f'http://127.0.0.1:8000/api/user/activate/{uid}/{token}/'

    message = (
        f"Hi,\n\n"
        f"Thank you for registering at Charity.\n"
        f"Please activate your account by visiting the link below:\n\n"
        f"{activation_link}\n\n"
        f"If you did not request this, you can safely ignore this email.\n\n"
        f"Best regards,\nCharity Team"
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
