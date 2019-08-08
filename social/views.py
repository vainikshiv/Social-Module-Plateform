from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login as auth_login,logout
from .forms import SignUpForm,PhotoForm
from django.contrib.auth.models import User
from .models import Profile,Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.country = form.cleaned_data.get('country')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            subject = 'Account has been created.'
            message = 'Thank you for register with us.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get('email'), ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request,'You have register successfully.')
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def login(request):
    if request.method == "POST":
        d = request.POST
        print(d)
        username = d['username']
        print(username)
        password = d['password']
        print(password)

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            print('success')
            messages.success(request, 'Login success.')
            return render(request,'dashboard.html')
        else:
            print('wrong')
            messages.error(request, 'Invalid username and password.')
            return redirect('social:login')
    return render(request,'registration/login.html')

# @login_required()
def dashboard(request):
    user = request.user
    posts = Post.objects.all()
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    print(posts)
    return render(request,'dashboard.html',{'user': user, 'posts': posts})

# @login_required()
def profile(request):
    user = request.user
    return render(request,'profile.html',{'user':user})

#@login_required()
def editProfile(request):
    u_id = request.user.id
    print('User id-',u_id)
    user = request.user
    if request.method == 'POST':
        d =request.POST.get
        print(d)
        image = request.FILES.get('image')
        print(image)
        form = PhotoForm(request.POST, request.FILES)
        if image:
            if form.is_valid():
                form.save()
                return redirect('photo_list')
            else:
                form = PhotoForm()
            return render(request, 'album/photo_list.html', {'form': form, 'photos': image})
        first_name=d('first_name');last_name=d('last_name');gender=d('gender');email=d('email')
        birth_date = d('birth_date'); city = d('city'); state = d('state'); country = d('country');address = d('address')
        if first_name != '':
            print(User.objects.filter(id=u_id).update(first_name=first_name))
            messages.success(request, 'Profile update successfully.')
        if last_name!= '':
            print(User.objects.filter(id=u_id).update(last_name=last_name))
            messages.success(request, 'Profile update successfully.')
        if email != '':
            print(User.objects.filter(id=u_id).update(email=email))
            messages.success(request, 'Profile update successfully.')
        if birth_date != '':
            print(Profile.objects.filter(id=u_id).update(birth_date=birth_date))
            messages.success(request, 'Profile update successfully.')
        if gender != '':
            print(Profile.objects.filter(id=u_id).update(gender=gender))
            messages.success(request, 'Profile update successfully.')
        if city != '':
            print(Profile.objects.filter(id=u_id).update(city=city))
            messages.success(request, 'Profile update successfully.')
        if state != '':
            print(Profile.objects.filter(id=u_id).update(state=state))
            messages.success(request, 'Profile update successfully.')
        if country != '':
            print(Profile.objects.filter(id=u_id).update(country=country))
            messages.success(request, 'Profile update successfully.')
        if address != '':
            print(Profile.objects.filter(id=u_id).update(fullAddress=address))
            messages.success(request, 'Profile update successfully.')
        return redirect('social:profile')

    return render(request,'editProfile.html',{'user':user})


def forgot_password(request):
    if request.method == 'POST':
        u_email= request.POST.get('email')
        user = User.objects.filter(email=u_email).first()
        print('User email-',user )
        if user is not None:
            print('Username exits')
            subject = 'Your account details'
            message = 'Your username is '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['@gmail.com', ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'User email-id found.')
        else:
            print('Not exits. please register.')
            messages.warning(request, 'User not register. Please register first.')
            return redirect('social:signup')
    return render(request,'registration/forgot_password.html')

