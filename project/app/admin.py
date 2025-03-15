from django.contrib import admin
from .models import Record, Configuration

# Register the Record and Configuration model with the admin site
admin.site.register(Record)
admin.site.register(Configuration)
