from django.contrib.auth.models import User
from odoo_auth.models import OdooUser
from odoo_auth.settings import *
import xmlrpclib
import logging
logger = logging.getLogger(__name__)


class OdooBackend(object):

    ODOO_SERVER_URL = None
    ODOO_SERVER_PORT = None
    ODOO_SERVER_DBNAME = None
    ODOO_SOCK_COMMON = None

    def __init__(self):
        self.ODOO_SERVER_URL = ODOO_SERVER_URL
        self.ODOO_SERVER_PORT = ODOO_SERVER_PORT
        self.ODOO_SERVER_DBNAME = ODOO_SERVER_DBNAME

        if not self.ODOO_SERVER_PORT:
            #If ODOO_SERVER_PORT == 0 or False, you use port standard 80
            url_login = ''.join([self.ODOO_SERVER_URL, '/xmlrpc/common'])
        else:
            url_login = ''.join([self.ODOO_SERVER_URL, ':', self.ODOO_SERVER_PORT, '/xmlrpc/common'])
        self.ODOO_SOCK_COMMON = xmlrpclib.ServerProxy(url_login)

    def authenticate(self, username=None, password=None):
        user = None
        try:
            odoo_id = self.ODOO_SOCK_COMMON.login(self.ODOO_SERVER_DBNAME, username, password)
            if odoo_id:
                try:
                    odoo_user = OdooUser.objects.get(odoo_id=odoo_id)
                    if odoo_user.username != username:
                        odoo_user.username = username
                        odoo_user.save()
                    user = odoo_user.user
                except OdooUser.DoesNotExist:
                    user, created = User.objects.get_or_create(username=username)
                    user.save()
                    odoo_user = OdooUser(user=user, username=username, odoo_id=odoo_id)
                    odoo_user.save()
        except Exception, e:
            logger.error('Exception with Odoo authentificate : %s' % e)
            return None
        return user

    def get_user(self, user_id):
        try:
            return OdooUser.objects.get(user=user_id).user
        except OdooUser.DoesNotExist:
            logger.error('No Odoo user identified with id : %s' % user_id)
            return None