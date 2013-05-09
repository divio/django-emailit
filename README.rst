==============
django-emailit
==============

TODO: make the docs nicer

Deadsimple html email sending.

add ``emailit`` for the bundled templates and ``absolute`` for easy full absolute urls to ``INSTALLED_APPS``.

usage::

  import emailit.api
  context = {
      'my_obj': 'whatever',
  }
  emailit.api.send_mail(['email@domain.com'], context, 'mymails/example_email')

now add these templates::

  mymails/example_email.body.html
  mymails/example_email.body.txt
  mymails/example_email.subject.txt

the convention is, that the body templates should extend ``emailit/base_email.body.html`` /
``emailit/base_email.body.txt`` and overrid the ``content`` block. This makes it easy to provide a site-wide look
to all emails using this system by overriding ``emailit/base_email.body.*``.

If the ``body.html`` template is not found, a simple text email is sent. If the ``body.txt`` template is missing,
it will be a pure html email.

HTML emails are passed through ``premailer``.

``language`` can be passed into the ``send_mail`` function to override the active language while rendering the mail.

The body templates will contain the rendered ``subject`` variable in their context. ``subject`` can also be passed directly into
``send_mail``.
