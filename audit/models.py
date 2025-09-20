from django.db import models
from django.utils.timezone import now

class LoginLog(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    login_time = models.DateTimeField(default=now)
    auth_mode = models.CharField(max_length=50)
    success = models.BooleanField(default=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {'✅' if self.success else '❌'} - {self.login_time}"
