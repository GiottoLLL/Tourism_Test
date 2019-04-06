from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _
import xadmin


class XAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'xadmin'
    verbose_name = _("Administration")

    def ready(self):
        self.module.autodiscover()
        setattr(xadmin,'site',xadmin.site)


# 更改侧边栏
# class UsersConfig(AppConfig):
#     name = 'users'
#     verbose_name = '用户信息'