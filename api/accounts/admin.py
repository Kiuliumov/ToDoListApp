from django.contrib import admin

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    ...

admin.site.register(AccountAdmin)
