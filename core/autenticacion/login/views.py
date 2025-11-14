from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages


class CustomLoginView(LoginView):
  template_name = "login.html"
  redirect_authenticated_user = True

  def post(self, request, *args, **kwargs):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect("home")    # redirige a dashboard o home
    else:
      messages.error(request, "Credenciales incorrectas.")
      return render(request, self.template_name, {
          "error": True,
      })
