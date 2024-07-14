from celery import shared_task
import time
from django.core.mail import send_mail
from decouple import config
from .models import CustomUser
from recipe.models import Recipe


@shared_task(bind=True) #TODO Fix me (raises all alone warning)
def send_daily_mail_like_count(self):
    """
    Sends daily emails to each author with the like counts for their recipes.

    This task runs as a scheduled job (via Celery Beat) and retrieves all authors 
    (CustomUser). For each author, it collects their recipes and calculates the 
    total likes for each. The results are emailed to the author.

    Returns:
        None
    """
    authors = CustomUser.objects.all()
    for author in authors:
        # Prepare a list to hold the recipe details
        recipe_details = []
        
        # Get all recipes for the author
        recipes = author.recipes.all()
        
        for recipe in recipes:
            total_likes = recipe.get_total_number_of_likes()
            recipe_details.append(f"{recipe.title}: {total_likes} likes")

        # Prepare the email
        subject = 'Daily Recipe Likes Update'
        message = f'Dear {author.username},\n\nHere is the like count for your recipes today:\n\n' + "\n".join(recipe_details)
        email_from = config('EMAIL_USER')
        recipient_list = [author.email]
        
        # Send the email
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False,
        )
        