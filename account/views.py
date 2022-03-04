from re import split
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm
from account.models import Account


import requests


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request=request)
            mail_subject = "Activate your blog account."
            message = render_to_string(
                "account/active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration",
            )
            return redirect("account:register")
        else:
            messages.error(request=request, message="Register failed!")
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")
            redirect("blog:post_list")

        else:
            messages.error(request=request, message="Login failed!")
    context = {
        "email": email if "email" in locals() else "",
        "password": password if "password" in locals() else "",
    }
    return render(request, "account/login.html", context=context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect("account:login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!"
        )
        return render(request, "account/login.html")
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect("blog:post_list")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "account/dashboard.html")


def forgotPassword(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request=request)
            mail_subject = "Reset your password"
            message = render_to_string(
                "account/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request=request,
                message="Password reset email has been sent to your email address",
            )
    except Exception:
        messages.error(request=request, message="Account does not exist!")
    finally:
        context = {
            "email": email if "email" in locals() else "",
        }
        return render(request, "account/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request=request, message="Please reset your password")
        return redirect("account:reset_password")
    else:
        messages.error(request=request, message="This link has been expired!")
        return redirect("blog:post_list")


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect("acount:login")
        else:
            messages.error(request, message="Password do not match!")
    return render(request, "account/reset_password.html")
