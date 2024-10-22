from email.mime.image import MIMEImage
import smtplib, ssl
import os
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Party, MEALS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.utils import make_msgid
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt


INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'
SMPT_SERVER = "smtp.gmail.com"
PORT = 587  # For starttls

def guess_party_by_invite_id_or_404(invite_id):
    try:
        return Party.objects.get(invitation_id=invite_id)
    except Party.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Party.objects.get(id=int(invite_id))
        else:
            raise Http404()


def get_invitation_context(party):
    return {
        'title': "Lion's Head",
        'main_image': 'bride-groom.png',
        'main_color': '#fff3e8',
        'font_color': '#666666',
        'page_title': "Eden and David - You're Invited!",
        'preheader_text': "You are invited!",
        'invitation_id': party.invitation_id,
        'party': party,
        'meals': MEALS,
    }

def send_invitation_email(party, test_only=False, recipients=None, unique_addresses_only=False):
    from redmail import EmailSender
    if recipients is None:
        recipients = party.guest_emails
    if not recipients:
        print('===== WARNING: no valid email addresses found for {} ====='.format(party))
        return
    if unique_addresses_only:
        # Remove duplicate emails within this party party
        recipients = list(dict.fromkeys(recipients))
    print(recipients)
    # server = smtplib.SMTP(SMPT_SERVER, PORT)
    # context = ssl.create_default_context()
    # server.starttls(context=context) # Secure the connection
    # server.ehlo() # Can be omitted
    # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    email = EmailSender(host=SMPT_SERVER, port=PORT, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    context = get_invitation_context(party)
    context['email_mode'] = True
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    # template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = f"""\
    Subject: WEDDING !!!
    You're invited to {settings.BRIDE_AND_GROOM}'s wedding. To view this invitation, visit {settings.WEDDING_WEBSITE_URL + reverse('invitation', args=[context['invitation_id']])} in any browser
    """
    subject = "You're invited"
    msg = MIMEMultipart('related')
    msg['From'] = settings.DEFAULT_WEDDING_FROM_EMAIL
    # msg['To'] = 'To Person <to@todomain.com>'
    msg['Subject'] = subject
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    part2 = MIMEText(template_html, 'html')
    msg.attach(part2)   
    # subject = "You're invited"
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    print(part2)
    attachment_cid = make_msgid()
    msg = EmailMessage()
    msg.set_content(template_html, "html")
    for filename in (context['main_image'], ):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'invitation', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg.add_related(
        image_file.read(), 'image', 'png', cid=attachment_cid)
            # msg_img = MIMEImage(image_file.read())
            # msg_img.add_header('Content-ID', '<{}>'.format(filename))
            # msg.attach(msg_img)
    
        # img = mpimg.imread(attachment_path)
        # imgplot = plt.imshow(img)
        # plt.show()
    email.send(
        sender=settings.DEFAULT_WEDDING_FROM_EMAIL,
        receivers=recipients,
        subject=subject,
        html="""
        <h1>Look at this:</h1>
        {{ my_image }}
        """,
        body_images={"my_image": attachment_path}
    )
    # server.sendmail(settings.DEFAULT_WEDDING_FROM_EMAIL, recipients, msg.as_string())
    # print(msg.as_string())
    print('sending invitation to {} ({})'.format(party.name, ', '.join(recipients)))

def send_invitation_email_django(party, test_only=False, recipients=None, unique_addresses_only=False):
    if recipients is None:
        recipients = party.guest_emails
    if not recipients:
        print ('===== WARNING: no valid email addresses found for {} ====='.format(party))
        return
    if unique_addresses_only:
        # Remove duplicate emails within this party party
        recipients = list(dict.fromkeys(recipients))
    print(recipients)

    context = get_invitation_context(party)
    context['email_mode'] = True
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = "You're invited to {}'s wedding. To view this invitation, visit {} in any browser.".format(
        settings.BRIDE_AND_GROOM,
        settings.WEDDING_WEBSITE_URL + reverse('invitation', args=[context['invitation_id']])
    )
    subject = "You're invited"
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, settings.DEFAULT_WEDDING_FROM_EMAIL, recipients,
                                 cc=settings.WEDDING_CC_LIST,
                                 reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['main_image'], ):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'invitation', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print('sending invitation to {} ({})'.format(party.name, ', '.join(recipients)))
    if not test_only:
        msg.send()


def send_all_invitations(test_only, mark_as_sent):
    to_send_to = Party.in_default_order().filter(is_invited=True, invitation_sent=None).exclude(is_attending=False)
    print(to_send_to)
    for party in to_send_to:
        send_invitation_email(party, test_only=test_only)
        if mark_as_sent:
            party.invitation_sent = datetime.now()
            party.save()
