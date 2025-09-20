from django.contrib import admin
from django.http import HttpResponse
from .models import LoginLog
import csv

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ("username", "auth_mode", "success", "login_time", "ip_address")
    list_filter = ("auth_mode", "success", "login_time")
    search_fields = ("username", "ip_address", "user_agent")
    ordering = ("-login_time",)
    actions = ["export_as_csv"]

    @admin.action(description="📤 Exportar registros seleccionados como CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=login_logs.csv"

        writer = csv.writer(response)
        writer.writerow(["Username", "Auth Mode", "Success", "Login Time", "IP Address", "User Agent"])

        for log in queryset:
            writer.writerow([
                log.username,
                log.auth_mode,
                "Sí" if log.success else "No",
                log.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                log.ip_address,
                log.user_agent or ""
            ])

        return response
