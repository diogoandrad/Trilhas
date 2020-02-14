from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):

    message_html = render_to_string(template_name, context) #transforma o html numa string

    message_txt = striptags(message_html) #retira as tags html

    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=recipient_list
    )

    email.attach_alternative(message_html, "text/html") #anexa o html no email
    email.send(fail_silently=fail_silently)

def send_mail(convite):
    subject = 'Convite Trilhas Fábrica'
    context = {
        'nome': convite.name,
        'email': convite.email,
        'token': convite.token,
    }
    template_name = 'convite/convite_email_content.html'

    send_mail_template(subject, template_name, context, [context['email']], settings.CONTACT_EMAIL)
