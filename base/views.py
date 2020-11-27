from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.views import generic

from .models import Profile
from .forms import CreateForm
from .models import Create

from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import datetime
from datetime import date
from django.utils import timezone

import stripe

stripe.api_key = "sk_test_51Hi3ccIhinpgN0d6E5B0qQhpblefy2DpeJEsa3Ctw8K5B0CN8J8rbziZBfDYwmiInTgFaSlyn8I6lmmUKDhDsBh100Woe7EF7v"

class FirstLoginView(LoginRequiredMixin, generic.TemplateView):
    model = Profile
    template_name = 'base/first_login.html'
    context_object_name = "profile"

    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You must login first."


class HomeView(LoginRequiredMixin, generic.ListView):
    model = Create
    template_name = 'base/home.html'
    context_object_name = "event_list"

    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You must login first."

    def get_queryset(self):
        now = timezone.now()
        return Create.objects.filter(Datetime__gte=now).order_by('Datetime')
        #return Create.objects.all().filter(Datetime__gte=datetime.datetime.now())


class VolunteerView(LoginRequiredMixin, generic.ListView):
    model = Create
    template_name = 'base/volunteer_view.html'
    context_object_name = "event_list"

    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You must login first."

    def get_queryset(self):
        now = timezone.now()
        return Create.objects.all().filter(Event='Volunteer').filter(Datetime__gte=now).order_by('Datetime')

class DonateView(LoginRequiredMixin, generic.ListView):
    model = Create
    template_name = 'base/donate_view.html'
    context_object_name = "event_list"

    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You must login first."

    def get_queryset(self):
        now = timezone.now()
        return Create.objects.all().filter(Event='Donation').filter(Datetime__gte=now).order_by('Datetime')

class AboutView(LoginRequiredMixin, generic.TemplateView):
    model = Profile
    template_name = 'base/about.html'

class LeaderboardView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'base/leaderboard.html'

    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You must login first."

    def get_queryset(self):
        return Profile.objects.all().order_by('-exp')[:10]

@login_required
def first_login(request):
    Profile.objects.get_or_create(user=request.user)
    #if first time logging in, redirect to first login page instead of home
    if not request.user.profile.first_login:
        return HttpResponseRedirect(reverse("base:home"))

    request.user.profile.first_login = False
    request.user.save()
    return render(request, "base/first_login.html")

#tutorial for google login followed from https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
def google_login(request):
    return render(request, "base/index.html")


@login_required
def signout(request):
    logout(request)
    return render(request, "base/index.html")


@login_required
def profile(request):
    request.user.profile.level = request.user.profile.exp // 1000
    event_history = request.user.profile.event_history.all()
    return render(request, 'base/profile.html', {'events': event_history})

@login_required()
def schedule(request):
    now = timezone.now()
    schedule = request.user.profile.event_history.all().filter(Event='Volunteer').filter(Datetime__gte=now)
    return render(request, 'base/schedule.html', {'schedule': schedule})

@login_required()
def accepted_task(request, pk):
    task = Create.objects.get(pk=pk)
    return render(request, 'base/accepted_task.html', {
        'event': task
    })

#After user logs in first time, they submit their preference for how they want to use site
@login_required()
def preference(request):
    #checks if user wants to be a volunteer, submitting otherwise
    if request.POST["Preference"] == "Volunteer":
        request.user.profile.is_volunteer = True
    else:
        request.user.profile.is_volunteer = False

    request.user.save()
    return HttpResponseRedirect(reverse("base:home"))

@login_required()
def create_offer(request):
    if request.user.profile.is_volunteer == True:
        messages.info(request, ('Sorry! The create page is not for volunteers and is only for submitters!'))
        return HttpResponseRedirect(reverse("base:home"))
    #post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        event = Create()
        event.Name = request.POST['Name']
        event.Description = request.POST['Description']
        event.Event = request.POST['Event']
        event.Date = request.POST['Date']
        event.Time = request.POST['Time']
        event.duration = request.POST['duration']
        event.Datetime = datetime.datetime.strptime(event.Date + " " + event.Time, "%Y-%m-%d %H:%M")
        #scale xp earned to duration of event if event is for volunteering
        if event.Event == 'Volunteer':
            event.xp = event.xp * int(event.duration)
            email = EmailMessage(
                "Successful Submitted Opportunity",
                'Dear ' + request.user.first_name + ",\n\nThank you for submitting the opportunity \"" + event.Name + "\"! To inform the volunteer(s) "
                "of any further details of the event (such as location, important updates, etc.), be sure to find the contacts of "
                "each of the volunteers under the \"Submitted Events\" tab on our site and then clicking the opportunity you created. "
                "\n\nSincerely,\nTeam Split Coin",
                'teamsplitcoin@gmail.com',
                [request.user.email],
            )
            email.fail_silently = False
            email.send()
        event.save()
        if event.Event == 'Volunteer':
            request.user.profile.submitted_volunteer.add(event)
        else:
            request.user.profile.submitted_donation.add(event)
            email = EmailMessage(
                "Successful Submitted Opportunity",
                'Dear ' + request.user.first_name + ",\n\nThank you for submitting the opportunity \"" + event.Name +
                "\"! To view how much money you have received for this donation opportunity, be sure to view the \"Submitted Events\" "
                "tab on our site and view the opportunity you have just created."
                "\n\nSincerely,\nTeam Split Coin",
                'teamsplitcoin@gmail.com',
                [request.user.email],
            )
            email.fail_silently = False
            email.send()
        return HttpResponseRedirect(reverse("base:home"))
    return render(request, 'base/create.html')

@login_required()
def show_task(request, pk):
    task = Create.objects.get(pk=pk)
    return render(request, 'base/task_view.html', {
        'event': task
    })

@login_required
def transaction(request, pk):
    if request.method == "POST":
        amount = float(request.POST['amount'])

        #from Stripe API
        customer = stripe.Customer.create(
            email = request.user.email,
            name = request.user.first_name,
            source = "tok_visa",
        )
        charge = stripe.Charge.create(
            customer = customer,
            amount = int(amount*100),
            currency = "usd",
            description = "Donation",
        )

        event = Create.objects.get(pk=pk)

        #scale xp earned to amount donated
        request.user.profile.exp += int(event.xp * amount)
        request.user.profile.level = request.user.profile.exp // 1000
        request.user.profile.event_history.add(event)

        event.amount_received += amount
        event.save()

        request.user.save()

    return redirect("base:success", args=amount, pk=pk)


@login_required()
def vsuccess(request, pk):
    if request.method == "POST":
        event = Create.objects.get(pk=pk)
        event.signup_list.add(request.user)

        if event in request.user.profile.event_history.all():
            messages.info(request, ('Sorry! You have already signed up for this event!'))
            return render(request, "base/vsuccess.html")

        email = EmailMessage(
            'Successful Volunteer Sign-Up',
            'Dear ' + request.user.first_name + ",\n" +
            "\nThank you for signing up for a volunteering opportunity! Here are the details of the event:" +
            "\n\nDate of event: " + str(event.Date) +
            "\nTime of event: " + str(event.Time) +
            "\nName of event: " + event.Name +
            "\nEvent description: " + event.Description +

            "\n\nSincerely,\nTeam Split Coin",
            'teamsplitcoin@gmail.com',
            [request.user.email],
        )
        email.fail_silently = False
        email.send()
        request.user.profile.exp += event.xp
        request.user.profile.level = request.user.profile.exp // 1000
        request.user.profile.event_history.add(event)

        request.user.save()
        event.save()

        return render(request, "base/vsuccess.html")


@login_required()
def success(request, args, pk):
    amount = args
    email = EmailMessage(
        'Successful Donation',
        'Dear ' + request.user.first_name + ",\n\nThank you for your $" + amount + " donation! \n\nSincerely,\nTeam Split Coin",
        'teamsplitcoin@gmail.com',
        [request.user.email],
    )
    email.fail_silently = False
    email.send()

    return render(request, "base/success.html", {"amount": amount})

@login_required()
def edit_profile(request):
    return render(request, "base/editprofile.html")

@login_required()
def save_edit(request):
    if 'Preference' in request.POST:
        if request.POST["Preference"] == "Volunteer":
            request.user.profile.is_volunteer = True
        else:
            request.user.profile.is_volunteer = False
    if 'phoneNum' in request.POST:
        request.user.profile.phoneNum = request.POST['phoneNum']

    request.user.save()
    return HttpResponseRedirect(reverse("base:profile"))

@login_required()
def submitted_events(request):
    if request.user.profile.is_volunteer == True:
        messages.info(request, ('Sorry! The submitted events page is not for volunteers and is only for submitters!'))
        return HttpResponseRedirect(reverse("base:home"))

    now = timezone.now()

    donations = request.user.profile.submitted_donation.all()
    volunteers = request.user.profile.submitted_volunteer.all().filter(Datetime__gte=now)
    return render(request, 'base/submitted_events.html', {'donations': donations, 'volunteers': volunteers})

@login_required()
def submitted_volunteer_view(request, pk):
    event = Create.objects.get(pk=pk)
    signup_list = event.signup_list.all()
    return render(request, 'base/submitted_task_view.html', {'event': event, 'list': signup_list})
