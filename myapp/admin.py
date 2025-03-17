from django.contrib import admin
from .models import CustomUser  
from .models import Category  
from .models import Plant ,Cart ,Order
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Plant)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)