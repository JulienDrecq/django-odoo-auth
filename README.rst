**Django Odoo Auth (Odoo backend with django)**

======================================

Django app for **Odoo (formerly OpenERP)** authentication.


Application development and testing with django v1.6.5


.. contents:: Contents
    :depth: 1

Quick start
-----------

1. Add ``odoo_auth`` to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'odoo_auth',
      )

2. Add ``backend`` to your AUTHENTICATION_BACKENDS setting like this::

    AUTHENTICATION_BACKENDS = (
        ...
        'odoo_auth.backends.OdooBackend',
    )
    
3. Edit the information to connect to your server Odoo in ``odoo_auth/settings.py`` ::

    ODOO_SERVER_URL = getattr(settings, 'ODOO_SERVER_URL', 'http://localhost')
    ODOO_SERVER_PORT = getattr(settings, 'ODOO_SERVER_PORT', 8069)
    ODOO_SERVER_DBNAME = getattr(settings, 'ODOO_SERVER_DBNAME', 'demo')

4. Run ``python manage.py syncdb`` to create the odoo_auth models.

5. For call ``odoo_auth``, use standard authenticate ::

    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)

6. Access in template to ``odoo_auth`` ::

    {{ user.odoouser.odoo_id }}
    {{ user.odoouser.username }}