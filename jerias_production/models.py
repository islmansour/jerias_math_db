from django.utils import timezone
from django.db import models


class Person(models.Model):
    lastName = models.CharField(max_length=255, null=True)
    firstName = models.CharField(max_length=255, null=True)
    startDate = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    parentPhone1 = models.CharField(max_length=255, null=True)
    parentPhone2 = models.CharField(max_length=255, null=True)
    dob = models.DateTimeField(null=True)
    userId = models.CharField(max_length=255, null=True)
    #createdBy = models.IntegerField(null=True)
    #created = models.DateTimeField(default=timezone.now)
    #lastUpdated = models.DateTimeField(default=timezone.now)
    # lastUpdatedBy = models.IntegerField(null=True):


class Group(models.Model):
    name = models.CharField(max_length=255)
    #teacherId = models.IntegerField(null=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    weekDays = models.CharField(max_length=255)
    type = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    createdBy = models.OneToOneField(
        'Person', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='created_group')
    created = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateTimeField(default=timezone.now)
    lastUpdatedBy = models.OneToOneField(
        'Person', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='updated_group')
    teacher = models.ForeignKey(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='group_teacher'
    )


class AppUser(models.Model):
    uid = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)
    active = models.BooleanField(null=True)
    contactId = models.IntegerField(null=True)
    createdBy = models.OneToOneField(
        'Person', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='created_appuser')
    created = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateTimeField(default=timezone.now)
    lastUpdatedBy = models.OneToOneField(
        'Person', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='updated_appuser')
    userType = models.CharField(max_length=255)
    language = models.CharField(max_length=255, null=True)
    admin = models.BooleanField(null=True)
    person = models.OneToOneField(
        'Person', null=True, on_delete=models.DO_NOTHING)


class GroupPerson(models.Model):
    studentId = models.IntegerField()
    groupId = models.IntegerField()
    createdBy = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='created_groupperson'
    )
    created = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateTimeField(default=timezone.now)
    lastUpdatedBy = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='updated_groupperson'
    )
    status = models.IntegerField(null=True)
    group = models.ForeignKey(
        'Group',
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='group_people'
    )
    student = models.ForeignKey(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='group_participations'
    )

    class Meta:
        unique_together = [('studentId', 'groupId')]


class GroupEvent(models.Model):
    created = models.DateTimeField(null=True)
    lastUpdated = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)

    # Foreign key relationships
    createdBy = models.ForeignKey(
        'Person', on_delete=models.DO_NOTHING, null=True, related_name='created_events')
    lastUpdatedBy = models.ForeignKey(
        'Person', on_delete=models.DO_NOTHING, null=True, related_name='updated_events')

    group = models.ForeignKey('Group', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"GroupEvent {self.pk}"


class StudentAttendance(models.Model):
    createdBy = models.IntegerField()
    created = models.DateTimeField()
    lastUpdated = models.DateTimeField()
    lastUpdatedBy = models.IntegerField()
    status = models.IntegerField()
    groupEvent = models.ForeignKey('GroupEvent', on_delete=models.CASCADE)
    student = models.ForeignKey('Person', on_delete=models.CASCADE)
