from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

#makes sure duration of event is at least 1 minute
def valid_duration(duration):
    if duration > 0:
        return duration
    else:
        raise ValidationError("Please enter a valid duration for the event in the number of minutes it will take to complete")

#Extension of User model through OneToOneField
class Create(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.TextField(max_length=300)
    Date = models.DateField(blank=True, null=True)
    Time = models.TimeField(blank=True, null=True)
    #type = [('Volunteer', 'Volunteer'), ('Donation', 'Donation')]
    Event = models.TextField(max_length=10)#, choices=type)
    xp = models.IntegerField(default=10)
    Datetime = models.DateTimeField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)

    #list of those who have signed up for event
    signup_list = models.ManyToManyField(User, blank=True)

    #total amount received if donation event
    amount_received = models.FloatField(default=0.0)

    def __str__(self):
        return self.Description

    def get_author(self):
        return self.Name

    def get_type(self):
        return self.Event

#how to extend profile model from User from tutorial at https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)
    phoneNum = models.CharField(max_length=20, blank=True)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=0) # Unsure if this will actually be used, not important at the moment.
    event_history = models.ManyToManyField(Create, related_name='event_history')

    #list of events submitted by user
    submitted_volunteer = models.ManyToManyField(Create, related_name='submitted_volunteer')
    submitted_donation = models.ManyToManyField(Create, related_name='submitted_donation')

    #true if user is a volunteer, false otherwise
    is_volunteer = models.BooleanField(default=True)

#automatically save and create Profile when User is created or modified
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

