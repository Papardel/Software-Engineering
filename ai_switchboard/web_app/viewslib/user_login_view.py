from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..forms import LoginForm
from django.contrib.auth import login, authenticate


# Login view. If the request method is POST, it tries to authenticate the user.
# If the user is authenticated, it returns a success message.
# If the user is not authenticated, it returns an error message.
# If the request method is not POST, it renders the 'login.html' template with a LoginForm instance.
def user_login_logic(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Username or password not provided")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout_logic(request):
    logout(request)
    return redirect('index')
