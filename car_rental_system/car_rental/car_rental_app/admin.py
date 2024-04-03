from django.contrib import admin

from . models import login,users,owners,vehicles,rent,booking,payment,items,images,feedback,chatz
# Register your models here.

admin.site.register(login)
admin.site.register(users)
admin.site.register(owners)
admin.site.register(vehicles)
admin.site.register(rent)
admin.site.register(booking)
admin.site.register(payment)
admin.site.register(items)
admin.site.register(images)
admin.site.register(feedback)
admin.site.register(chatz)
