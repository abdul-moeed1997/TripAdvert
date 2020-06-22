from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Person)
admin.site.register(models.User)
admin.site.register(models.Organizer)
admin.site.register(models.Event)
admin.site.register(models.Review)
admin.site.register(models.Message)
admin.site.register(models.Question)
admin.site.register(models.Answer)
#admin.site.register(models.Notification)
admin.site.register(models.BlockRequest)
admin.site.register(models.Booking)
admin.site.register(models.Image)


