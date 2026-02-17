from django.contrib import admin
from . models import perfume 
from . models import PerfumeDetail,new,Cart,Order,Profile
admin.site.register(perfume)
admin.site.register(new)
admin.site.register(PerfumeDetail)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(Order)



