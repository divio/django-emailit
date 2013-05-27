# -*- coding: utf-8 -*-
import premailer
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, mail_admins, mail_managers
from django.template import Context, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import translation
from emailit.utils import force_language


def construct_mail(recipients=None, context=None, template_base='emailit/email', subject=None, message=None, site=None,
                   subject_template=None, body_template=None, html_template=None, from_email=None, language=None,
                   **kwargs):
    """
    usage:
    construct_mail(['my@email.com'], {'my_obj': obj}, template_base='myapp/emails/my_obj_notification').send()
    :param recipients: list of recipients
    :param context: context for template rendering
    :param template_base: the base template. '.subject.txt', '.body.txt' and '.body.html' will be added
    :param subject: optional subject instead of rendering it through a template
    :param message: optional message (will be inserted into the base email template)
    :param site: the site this is on. uses current site by default
    :param subject_template: override the subject template
    :param body_template: override the body template
    :param html_template: override the html body template
    :param from_email: defaults to settings.DEFAULT_FROM_EMAIL
    :param language: the language that should be active for this email. defaults to currently active lang
    :param kwargs: kwargs to pass into the Email class
    :return:
    """
    language = language or translation.get_language()
    with force_language(language):
        recipients = recipients or []
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        subject_template = subject_template or '%s.subject.txt' % template_base
        body_template = body_template or '%s.body.txt' % template_base
        html_template = html_template or '%s.body.html' % template_base

        if context:
            context = Context(context)
        else:
            context = Context({})

        site = site or Site.objects.get_current()
        context['site'] = site
        protocol = 'http'  # TODO: this should come from settings
        base_url = "%s://%s" % (protocol, site.domain)
        if message:
            context['message'] = message

        subject = subject or render_to_string(subject_template, context)
        subject = subject.replace('\n', '').replace('\r', '').strip()
        context['subject'] = subject
        try:
            html = render_to_string([html_template, 'emailit/empty.txt'], context)
            html = premailer.transform(html, base_url=base_url)
        except TemplateDoesNotExist, e:
            html = ''
        try:
            body = render_to_string([body_template, 'emailit/empty.txt'], context)
        except TemplateDoesNotExist, e:
            body = ''

        mail = EmailMultiAlternatives(subject, body, from_email, recipients, **kwargs)

        if not (body or html):
            # this is so a meaningful exception can be raised
            render_to_string([html_template], context)
            render_to_string([body_template], context)

        if html:
            mail.attach_alternative(html, 'text/html')
    return mail


def send_mail(*args, **kwargs):
    return construct_mail(*args, **kwargs).send()


def mail_admins(*args, **kwargs):
    return send_mail([a[1] for a in settings.ADMINS], *args, **kwargs)


def mail_managers(*args, **kwargs):
    return send_mail([a[1] for a in settings.MANAGERS], *args, **kwargs)