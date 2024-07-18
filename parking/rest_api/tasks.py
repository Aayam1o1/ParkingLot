from celery import shared_task
from django.core.mail import send_mail
import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)
html_content = render_to_string('email_template.html')

@shared_task
def send_registration_email(email):
    print('ureeeeeeeee')
    print(email, "email")
    try:
        send_mail(
            'Registration Successful',
            'Thank you for registering!',
            'nepalicious.webapp@gmail.com',
            [email],
            fail_silently=False,
        )
        logger.info(f"Sent registration email to {email}")
    except Exception as e:
        logger.error(f"Failed to send registration email to {email}: {str(e)}")

       
        # html_content = render_to_string('email_template.html')  # Ensure email_template.html exists and is correctly formatted
        # email_msg = EmailMessage(
        #     'Registration Successful',  # Subject
        #     html_content,                # HTML content
        #     'nepalicious.webapp@gmail.com',     # From email address
        #     [email],                     # To email addresses
        # )
        # email_msg.content_subtype = "html"
        # email_msg.send()
        # logger.info(f"Sent registration email to {email}")