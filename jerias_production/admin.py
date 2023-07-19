from django import forms
from django.contrib import admin
from .models import Group, Account, GroupEvent, GroupPerson, LookupTable, Payment, Person, AppUser, Purchase, PurchaseAttendance, StudentAttendance


admin.site.register(Account)

#
admin.site.register(AppUser)
admin.site.register(GroupEvent)
admin.site.register(Payment)
admin.site.register(Group)


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdBy', 'created', 'lastUpdated',
                    'lastUpdatedBy', 'status', 'groupEvent', 'student']


admin.site.register(StudentAttendance, StudentAttendanceAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdBy', 'created', 'lastUpdated', 'lastUpdatedBy', 'status',
                    'student', 'amount', 'maxAttendances', 'account', 'autoGenerate', 'noMoreEventsAllowed',
                    'allPurchaseAttendancesB', 'purchaseAttendancesBillable']

    # Optionally, you can define a method to display the value of the @property 'noMoreEventsAllowed'
    def noMoreEventsAllowed(self, obj):
        return obj.noMoreEventsAllowed
    # If 'noMoreEventsAllowed' is a boolean property
    noMoreEventsAllowed.boolean = True


admin.site.register(Purchase, PurchaseAdmin)


class PurchaseAttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase', 'studentAttendance', 'created']


admin.site.register(PurchaseAttendance, PurchaseAttendanceAdmin)


class PersonAdminForm(forms.ModelForm):
    lastName = forms.CharField(max_length=255, required=False)
    firstName = forms.CharField(max_length=255, required=False)
    startDate = forms.DateTimeField(required=False)
    status = forms.IntegerField(required=False)
    phone = forms.CharField(max_length=255, required=False)
    email = forms.CharField(max_length=255, required=False)
    parentPhone1 = forms.CharField(max_length=255, required=False)
    parentPhone2 = forms.CharField(max_length=255, required=False)
    dob = forms.DateTimeField(required=False)
    userId = forms.CharField(max_length=255, required=False)
    type = forms.IntegerField(required=False)

    class Meta:
        model = Person
        fields = ['lastName', 'firstName', 'startDate', 'status', 'phone',
                  'email', 'parentPhone1', 'parentPhone2', 'dob', 'userId', 'type']


@admin.register(Person)
class PersoneAdmin(admin.ModelAdmin):
    form = PersonAdminForm


class LookupTableAdminForm(forms.ModelForm):
    desc = forms.CharField(max_length=2000, required=False)
    seq = forms.IntegerField(required=False)

    class Meta:
        model = LookupTable
        fields = ['code', 'type', 'value', 'seq', 'active', 'desc', 'lang']


@admin.register(LookupTable)
class LookupTableAdmin(admin.ModelAdmin):
    form = LookupTableAdminForm


@admin.register(GroupPerson)
class GroupPersonAdmin(admin.ModelAdmin):
    list_display = ('display_group_student', 'createdBy',
                    'created', 'lastUpdated')

    def display_group_student(self, obj):
        return f'{obj.groupId}-{obj.studentId}'
    display_group_student.short_description = 'Group-Student'
