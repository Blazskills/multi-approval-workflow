from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from account.models import User
from account.perms_constants import PERMS_CONSTANT_LIST


def get_content_type():
    try:
        return ContentType.objects.get_for_model(User)
    except:
        return None


def create_default_permissions():
    ct = get_content_type()
    # print(ct)
    if not ct:
        return
    for perm in PERMS_CONSTANT_LIST:
        perm_dict = dict(perm)
        for key, val in perm_dict.items():
            try:
                Permission.objects.get(codename=key, content_type=ct)
            except:
                Permission.objects.create(codename=key, name=val, content_type=ct)


def get_user_permissions(user):
    try:
        return list(user.get_all_permissions())
    except:
        return []


def get_user_permissions_new(user):
    try:
        from django.db.models import Q
        user_permissions = list(
            Permission.objects.filter(Q(user=user) | Q(group__user=user)).values_list('codename', flat=True))
        return user_permissions
    except:
        return []


def get_all_permission_list():
    try:
        perms = Permission.objects.filter(content_type__app_label=User._meta.app_label,
                                          content_type__model=User._meta.model_name).exclude(
            codename__in=['add_user', 'delete_user', 'change_user', 'view_user', 'outreach_officer']).order_by(
            'codename')
        return sorted(list(set([x.codename for x in perms])))
    except:
        return []


def delete_all_permission():
    perms = Permission.objects.filter(content_type__app_label=User._meta.app_label,
                                      content_type__model=User._meta.model_name)
    perms.delete()


def get_permission(codename):
    try:
        return Permission.objects.get(codename=codename)
    except:
        return None


def get_or_create_permission(codename, name=None):
    ct = get_content_type()
    try:
        p = Permission.objects.get(codename=codename, content_type=ct)
    except:
        p = Permission.objects.create(codename=codename, name=name, content_type=ct)
    return p


def get_perm_info(perm):
    perm_dict = dict(perm)
    for key, val in perm_dict.items():
        return key, val
