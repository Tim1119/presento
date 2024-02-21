# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def send_confirmation_email_task(email):
#     subject = 'Welcome to Our Website'
#     message = 'Thank you for signing up!'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
