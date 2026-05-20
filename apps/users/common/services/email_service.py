from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
    


# =========================================================
# SEND EMAIL (GENERIC)
# =========================================================
def send_email(subject, template_name, context, recipient_list):

    try:
        # render correct template with context
        html_content = render_to_string(template_name, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body="Please use HTML supported email client.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )

        email.attach_alternative(html_content, "text/html")

        email.send(fail_silently=False)

        return True, "Email sent successfully"

    except Exception as e:
        print(f"Error sending email: {e}")
        return False, str(e)


# =========================================================
# SEND OTP EMAIL
# =========================================================
def send_otp_email(email, otp):

    return send_email(
        subject="BTR Mall OTP Verification",
        template_name="emails/otp_email.html",
        context={
            "otp": otp,
            "app_name": "BTR Mall"
        },
        recipient_list=[email]
    )
    


def send_welcome_email(email, user_name):
    try:
        print(f"Sending welcome email to {email} for user {user_name}")

        return send_email(
            subject="Welcome to BTR Mall 🎉",
            template_name="emails/welcome_email.html",
            context={"user_name": user_name},
            recipient_list=[email]
        )    
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False, str(e)    