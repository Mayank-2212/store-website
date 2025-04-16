from django.shortcuts import render, redirect
from.models import Account
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
        except Account.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'signin.html')


@login_required(login_url="signin")
def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['password']
        c_passwd = request.POST['c_password']
        
        if not first_name or not last_name or not email or not passwd or not c_passwd:
            messages.error(request, 'Please fill all fields')
        elif Account.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists!')
        elif passwd!= c_passwd:    
            messages.error(request, "Passwords don't match!!")
        else:
            new_emp = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=passwd)
            new_emp.save()
            messages.success(request, 'User created successfully')
            current_site=get_current_site(request)
            mail_subject="Please activate your account"
            message=render_to_string('emails/account_verification.html',
                        {'user':new_emp,
                        'domain':current_site,
                        'uid':urlsafe_base64_encode(force_bytes(new_emp.pk)),
                        'token':default_token_generator.make_token(new_emp)})
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('signin')
    return render(request, 'register.html')


@login_required(login_url="signin")

def signout(request):
    logout(request)
    return redirect('signin')

def delivery_info(request):
    if request.method == 'POST':
        country = request.POST['country']
        state = request.POST['state']
        street = request.POST['street']
        building = request.POST['building']
        house = request.POST['house']
        postal_code = request.POST['postal_code']
        zip = request.POST['zip']
        user = Account.objects.get(id=request.user.id)

        user.country = country
        user.state = state
        user.street = street
        user.building = building
        user.house = house
        user.postal_code = postal_code
        user.zip = zip
        user.save()

    return redirect('')