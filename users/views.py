from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreationForm, LoginForm,ProfileUpdateForm
from django.contrib import messages



# Create your views here.

class RegisterView(View):
    def get(self, request):
        create_form = UserCreationForm()
        context = {
            "form":create_form
        }
        return render(request, "users/register.html",context)

    def post(self,request):
        create_form = UserCreationForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, "users/register.html", context)


class LoginView(View):
    def get(self, request):
        login_form=LoginForm()
        return render(request, "users/login.html", {'login_form': login_form})

    def post(self, request):
        login_form=AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user=login_form.get_user()
            login(request,user)
            messages.success(request,"You have sucessfully loged in")

            return redirect('books:list')
        else:
            return render(request, "users/login.html", {'login_form': login_form})

class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.info(request,"You have sacsessfully logout")
        return redirect('landing_page')
class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"users/profile.html")

class ProfileEditView(LoginRequiredMixin,View):
    def get(self,request):
        update_form = ProfileUpdateForm(instance=request.user)
        return render(request, "users/profile_edit.html",{"form": update_form})

    def post(self,request):
        update_form = ProfileUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "You have successfully update your profile")
            return redirect("users:profile")

        return render(request, "users/profile_edit.html",{"form": update_form})

