from django.contrib import admin
from .models import Profile,Wishlist,Cart,Order

# Register your models here.
admin.site.register(Profile)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
