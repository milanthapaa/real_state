from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


# Login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect.')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


# Register user
def register(request):
    if request.method == 'POST':
        # Get the value
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validations
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already taken.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You are now registered and can login.')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match.')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


# Logout user
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out.')
        return redirect('index')

    return redirect('index')


@login_required
def dashboard(request):
    user_id = request.user.id
    contacts = Contact.objects.order_by('-contact_date').filter(user_id=user_id)

    context = {
        'contacts': contacts
    }

    return render(request, 'accounts/dashboard.html', context)
