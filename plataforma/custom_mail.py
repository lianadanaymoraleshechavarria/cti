from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from .models import Email

def custom_send_mail():
    email = Email.objects.get(id=1)
    try:
            backend = EmailBackend(
                host=email.smtp_server,
                port=email.smtp_port,
                username=email.smtp_username,
                password=email.smtp_password,
                use_tls=False,
                use_ssl=True,
                fail_silently=False,
            )
            
            return backend
    except Exception as e:
        print(e)
        return None