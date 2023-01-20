def signUpPage(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # validates the form
            user = form.save()

            username = form.cleaned_data.get('username')
            Customer.objects.create(
                user=user,
            )  # creates a customer profile whenever they sign up.

            messages.success(
                request, 'Account Created Successfully for ' + username)
            return redirect('loginPage')
    context = {'form': form}
    return render(request, 'store/register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is not correct')
            # return render(request, 'store/login.html', context)

    context = {}
    return render(request, 'store/login.html', context)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'emmakolade',
        'USER': 'postgres',
        'PASSWORD': 'DjangoPost123#',
        'HOST': 'database-1.cvq3veqtqxbn.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
