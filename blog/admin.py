from django.contrib import admin

# Register your models here.



from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile', )

class GradeCourseAdmin(admin.ModelAdmin):
    list_display = ('grade_name','subject_name','term','price',)

class GradeAdmin(admin.ModelAdmin):
        list_display = ('name',)


class subjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(grade_course, GradeCourseAdmin)
admin.site.register(grade, GradeAdmin)
admin.site.register(subject, subjectAdmin)

