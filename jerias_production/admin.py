from django.contrib import admin
from .models import GroupEvent, GroupPerson, Person, AppUser, StudentAttendance


admin.site.register(Person)
admin.site.register(AppUser)
admin.site.register(GroupEvent)
admin.site.register(StudentAttendance)


@admin.register(GroupPerson)
class GroupPersonAdmin(admin.ModelAdmin):
    list_display = ('display_group_student', 'createdBy',
                    'created', 'lastUpdated')

    def display_group_student(self, obj):
        return f'{obj.groupId}-{obj.studentId}'
    display_group_student.short_description = 'Group-Student'
