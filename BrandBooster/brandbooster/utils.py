from . import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import string
import random
from django.utils.text import slugify

def send_email_for_user_account_activation(username, email):
    if settings.SERVER:
        link = settings.ALLOWED_HOSTS[0] + '/active/' + str(username) + '/'
    else:
        link = 'http://127.0.0.1:8000' + '/' + 'active' + '/' + str(username) + '/'

    html_message = render_to_string('mail_template.html', {'context': link})
    message = EmailMessage("Activate your Brand Booster account", html_message, settings.EMAIL_HOST_USER, [email])
    message.content_subtype = 'html'
    message.send()

def sendMail(otp,email):
    if settings.SERVER:
        link = settings.ALLOWED_HOSTS[0] + '/active/' + str(email) + '/'
    else:
        link = 'http://127.0.0.1:8000' + '/' + 'active' + '/' + str(email) + '/'

    html_message = render_to_string('mail_forget_template.html', {'context': otp})
    message = EmailMessage("Change Password OTP for Brand Booster account", html_message, settings.EMAIL_HOST_USER, [email])
    message.content_subtype = 'html'
    message.send()

# SLUG FIELD 
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.company_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug