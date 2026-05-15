from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_email(subject, html_content, recipient_list):

    try:

        email = EmailMultiAlternatives(
            subject=subject,
            body="OTP Verification",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )

        email.attach_alternative(
            html_content,
            "text/html"
        )

        email.send()

        return True, "Email sent"

    except Exception as e:
        return False, str(e)


def send_otp_email(email, otp):

    subject = "BTR Mall OTP Verification"

    html_content = render_to_string(
        "emails/otp_email.html",
        {
            "otp": otp
        }
    )

    return send_email(
        subject,
        html_content,
        [email]
    )
