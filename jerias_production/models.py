from django.utils import timezone
from django.db import models
import json


class Account(models.Model):
    name = models.CharField(max_length=255, null=True)
    startDate = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    endDate = models.DateTimeField(null=True)
    owner = models.ForeignKey(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='account_owner_data'

    )
    account = models.ForeignKey(
        'Account',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='groups'
    )

    def to_json(self):
        return {
            'name': self.name,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'status': self.status,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'owner': self.owner.to_json() if self.owner else None,
            'account': self.account.to_json() if self.account else None,
        }


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

    def to_json(self):
        return {
            'lastName': self.lastName,
            'firstName': self.firstName,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'status': self.status,
            'phone': self.phone,
            'email': self.email,
            'parentPhone1': self.parentPhone1,
            'parentPhone2': self.parentPhone2,
            'dob': self.dob.isoformat() if self.dob else None,
            'userId': self.userId,
        }


class Group(models.Model):
    name = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    weekDays = models.CharField(max_length=255)
    type = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    createdBy = models.OneToOneField(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='created_group'
    )
    created = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateTimeField(default=timezone.now)
    lastUpdatedBy = models.OneToOneField(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='updated_group'
    )
    teacher = models.ForeignKey(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='group_teacher'
    )

    def to_json(self):
        return {
            'name': self.name,
            'startDate': self.startDate.isoformat(),
            'endDate': self.endDate.isoformat(),
            'weekDays': self.weekDays,
            'type': self.type,
            'status': self.status,
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'created': self.created.isoformat(),
            'lastUpdated': self.lastUpdated.isoformat(),
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'teacher': self.teacher.to_json() if self.teacher else None,
        }


class AppUser(models.Model):
    uid = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)
    active = models.BooleanField(null=True)
    contactId = models.IntegerField(null=True)
    createdBy = models.OneToOneField(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='created_appuser'
    )
    created = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateTimeField(default=timezone.now)
    lastUpdatedBy = models.OneToOneField(
        'Person',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='updated_appuser'
    )
    userType = models.CharField(max_length=255)
    language = models.CharField(max_length=255, null=True)
    admin = models.BooleanField(null=True)
    person = models.OneToOneField(
        'Person',
        null=True,
        on_delete=models.DO_NOTHING
    )

    def to_json(self):
        return {
            'uid': self.uid,
            'token': self.token,
            'active': self.active,
            'contactId': self.contactId,
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'created': self.created.isoformat(),
            'lastUpdated': self.lastUpdated.isoformat(),
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'userType': self.userType,
            'language': self.language,
            'admin': self.admin,
            'person': self.person.to_json() if self.person else None,
        }


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

    def to_json(self):
        return {
            'studentId': self.studentId,
            'groupId': self.groupId,
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'created': self.created.isoformat(),
            'lastUpdated': self.lastUpdated.isoformat(),
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'status': self.status,
            'group': self.group.to_json() if self.group else None,
            'student': self.student.to_json() if self.student else None,
        }


class GroupEvent(models.Model):
    created = models.DateTimeField(null=True)
    lastUpdated = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)

    createdBy = models.ForeignKey(
        'Person',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='created_events'
    )
    lastUpdatedBy = models.ForeignKey(
        'Person',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='updated_events'
    )

    group = models.ForeignKey('Group', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"GroupEvent {self.pk}"

    def to_json(self):
        return {
            'created': self.created.isoformat() if self.created else None,
            'lastUpdated': self.lastUpdated.isoformat() if self.lastUpdated else None,
            'status': self.status,
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'group': self.group.to_json() if self.group else None,
        }


class StudentAttendance(models.Model):
    createdBy = models.IntegerField()
    created = models.DateTimeField()
    lastUpdated = models.DateTimeField()
    lastUpdatedBy = models.IntegerField()
    status = models.IntegerField()
    groupEvent = models.ForeignKey('GroupEvent', on_delete=models.CASCADE)
    student = models.ForeignKey('Person', on_delete=models.CASCADE)

    def to_json(self):
        return {
            'createdBy': self.createdBy,
            'created': self.created.isoformat(),
            'lastUpdated': self.lastUpdated.isoformat(),
            'lastUpdatedBy': self.lastUpdatedBy,
            'status': self.status,
            'groupEvent': self.groupEvent.to_json() if self.groupEvent else None,
            'student': self.student.to_json() if self.student else None,
        }


class Purchase(models.Model):
    createdBy = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='purchases_created')
    created = models.DateTimeField(null=True)
    lastUpdated = models.DateTimeField(null=True)
    lastUpdatedBy = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='purchases_updated')
    status = models.IntegerField(null=True)
    student = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    maxAttendances = models.IntegerField(null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    autoGenerate = models.BooleanField(default=False)

    def to_json(self):
        return {
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'created': self.created.isoformat() if self.created else None,
            'lastUpdated': self.lastUpdated.isoformat() if self.lastUpdated else None,
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'status': self.status,
            'student': self.student.to_json() if self.student else None,
            'amount': str(self.amount),
            'maxAttendances': self.maxAttendances,
            'account': self.account.to_json() if self.account else None,
            'autoGenerate': self.autoGenerate

        }


class Payment(models.Model):
    purchase = models.OneToOneField(
        Purchase, on_delete=models.CASCADE, primary_key=True, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='payments_created')
    lastUpdatedBy = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='payments_updated')
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    PAYMENT_TYPES = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('cheque', 'Cheque'),
        ('bit', 'Bit'),
    )
    paymentType = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    chequeNumber = models.CharField(max_length=50, blank=True)
    chequeBank = models.CharField(max_length=100, blank=True)
    chequeDate = models.DateTimeField(null=True)
    notes = models.CharField(max_length=2000, blank=True)

    def to_json(self):
        return {
            'purchase': self.purchase.to_json(),
            'amount': str(self.amount),
            'created': self.created.isoformat(),
            'lastUpdated': self.lastUpdated.isoformat(),
            'createdBy': self.createdBy.to_json() if self.createdBy else None,
            'lastUpdatedBy': self.lastUpdatedBy.to_json() if self.lastUpdatedBy else None,
            'account': self.account.to_json() if self.account else None,
            'paymentType': self.paymentType,
            'chequeNumber': self.chequeNumber,
            'chequeBank': self.chequeBank,
            'chequeDate': self.chequeDate.isoformat() if self.chequeDate else None,
            'notes': self.notes,
        }


class LookupTable(models.Model):
    code = models.IntegerField(null=True)
    type = models.CharField(max_length=20, null=True)
    value = models.CharField(max_length=20, null=True)
    seq = models.IntegerField(null=True)
    active = models.BooleanField(default=True)
    desc = models.CharField(max_length=2000, null=True)
    lang = models.CharField(max_length=3, null=True)

    class Meta:
        unique_together = [('type', 'code', 'lang')]

    def to_json(self):
        data = {
            'code': self.code,
            'type': self.type,
            'value': self.value,
            'seq': self.seq,
            'active': self.active,
            'desc': self.desc,
            'lang': self.lang,
        }
        return data

    def __str__(self):
        return f"LOV {self.type} {self.value} {self.lang}"
