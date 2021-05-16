from django.contrib import admin
from .models import Hospital
from .models import Producer
from .models import Transporter
from .models import Order
# Register your models here.
admin.site.register(Hospital)
admin.site.register(Producer)
admin.site.register(Transporter)
admin.site.register(Order)