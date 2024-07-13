from celery import shared_task
import time
from django.core.mail import send_mail
from decouple import config


@shared_task(bind=True)
def notify_userlogin_creation(self, recipe_id, data):
    # Here you can implement logic to notify users or log recipe creation
    time.sleep(15)
    print("login asdadad", data)
    
    print(f'Recipe {recipe_id} has been created.')  # Replace with actual logic
    
@shared_task(bind=True)
def send_daily_mail_like_count(self):
    user = config('EMAIL_USER')
    print(f'Sending email from: {user}')
    send_mail(
        'Celery Task Worked!',
        'This is the body of the email.',
        user,
        ['bilajo5443@cartep.com'],
    )
    print('Email should be sent')