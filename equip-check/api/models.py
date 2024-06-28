from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    ROLES = (
        ('Superadmin', 'Superadmin'),
        ('Suprevisor', 'Suprevisor'),
        ('employee', 'employee'),
    )
    STATIONARY = 1
    UPWARDS = 2
    DECLINE = 3
    NO_VALUE = 0
    STATUS = (
        (STATIONARY, 'Stationary'),
        (UPWARDS, 'Upwards'),
        (DECLINE, 'Decline'),
        (NO_VALUE, 'No_value')
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    roles = models.CharField(max_length=50, choices = ROLES, null=True)
    employee_supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    user_status = models.IntegerField(choices=STATUS, default=0)
    device_token = models.CharField(max_length=522, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    
    def __str__(self):
        return self.email


class Equipments(models.Model):
    name = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    image = models.ImageField(upload_to ='uploads/', null=True, blank=True)
    selected_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                related_name='selected_by')

    class Meta:
        db_table = 'equipments'
        verbose_name_plural = "Equipments"
        indexes = [
            models.Index(fields=['name'])
        ]

class SelectedEquipments(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
        related_name='user_id')
    selected_equipment = models.ManyToManyField(Equipments, related_name='selected_equipment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device_token = models.CharField(max_length=522, null=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'selectedequipments'
        verbose_name_plural = "Selected Equipments"

class NotificationQuerySet(models.QuerySet):
    def production_notifications(self):
        return self.filter(sandbox=False)

    def sandbox_notifications(self):
        return self.filter(sandbox=True)

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def production_notifications(self):
        return self.get_queryset().production_notifications()

    def sandbox_notifications(self):
        return self.get_queryset().sandbox_notifications()

class Notification(models.Model):
    sender = models.ForeignKey(User, related_name="notifications_sent", on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(User, related_name="notifications_received", on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=1000)
    type = models.CharField(max_length=16, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    sandbox = models.BooleanField(default=False, db_index=True)
    response_code = models.IntegerField(null=True, blank=True)

    notification_read= models.BooleanField(default=False)
    notifications = NotificationManager()
    objects = models.Manager()

    class Meta:
        ordering = ["-created_on"]