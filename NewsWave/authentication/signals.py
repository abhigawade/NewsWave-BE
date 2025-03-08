from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:  
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,  # Must be your verified email
            to_emails=instance.email,
            subject="Welcome to NewsWave!",
            html_content=f"""
            <p>Hi <strong>{instance.email}</strong>,</p>
            <p>Thank you for registering on <strong>NewsWave</strong>. Stay updated with the latest news!</p>
            <p>Best Regards,<br>NewsWave Team</p>
            """
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
            print(f" Welcome email sent")
        except Exception as e:
            print(f"Email sending failed: {e}")
