from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to NewsWave!"
        message = f"Hi {instance.email},\n\nThank you for registering on NewsWave. Stay updated with the latest news!\n\nBest Regards,\nNewsWave Team"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)
