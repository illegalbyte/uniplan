from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student_Profile)
admin.site.register(University)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Unit)
admin.site.register(Enrollments)
admin.site.register(Assignment)
admin.site.register(CoreSequence)
admin.site.register(MajorSequence)
admin.site.register(MinorSequence)
admin.site.register(UnitSet)