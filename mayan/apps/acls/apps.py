from __future__ import unicode_literals

from django import apps
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links
from project_setup.api import register_setup

from .classes import (
    AccessHolder, AccessObject, AccessObjectClass, ClassAccessHolder
)
from .links import (
    acl_class_acl_detail, acl_class_acl_list, acl_class_grant, acl_class_list,
    acl_class_new_holder_for, acl_class_revoke, acl_detail, acl_grant,
    acl_holder_new, acl_revoke, acl_setup_valid_classes
)
from .models import CreatorSingleton


def create_creator_user(sender, **kwargs):
    if kwargs.get('app') == 'acls':
        CreatorSingleton.objects.get_or_create()


class ACLsApp(apps.AppConfig):
    name = 'acls'
    verbose_name = _('ACLs')

    def ready(self):
        register_links([AccessObject], [acl_holder_new], menu_name='sidebar')
        register_links(AccessObjectClass, [acl_class_acl_list, acl_class_new_holder_for])
        register_links(AccessHolder, [acl_detail])
        register_links(['acls:acl_setup_valid_classes', 'acls:acl_class_acl_list', 'acls:acl_class_new_holder_for', 'acls:acl_class_acl_detail', 'acls:acl_class_multiple_grant', 'acls:acl_class_multiple_revoke'], [acl_class_list], menu_name='secondary_menu')
        register_links(ClassAccessHolder, [acl_class_acl_detail])
        register_links(['acls:acl_detail'], [acl_grant, acl_revoke], menu_name='multi_item_links')
        register_links(['acls:acl_class_acl_detail'], [acl_class_grant, acl_class_revoke], menu_name='multi_item_links')
        register_setup(acl_setup_valid_classes)

        post_migrate.connect(create_creator_user, dispatch_uid='create_creator_user')
