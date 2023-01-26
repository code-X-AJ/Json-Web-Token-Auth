from django.contrib import admin
from Authentication.models import User
from Authentication.models import Picture
# Register your models here.

# the custom user model is registered here
admin.site.register(User)

# the image model is registered here
admin.site.register(Picture)