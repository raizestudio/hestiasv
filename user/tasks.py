from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_activation_email(email, email_code):
    print("Sending activation email")
    subject = "Votre inscription Hestia!"
    from_email = "no-reply@hestia.com"
    to = [email]
    activation_link = f"http://localhost:3000/user/activate/{email_code}"
    text_content = f"Validez votre inscription en cliquant sur le lien suivant: {activation_link}"
    html_content = render_to_string("mail/activate_email.html", {"activation_link": activation_link})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
