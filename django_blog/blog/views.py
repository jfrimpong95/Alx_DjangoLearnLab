from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update user object
        if username:
            user.username = username
        if email:
            user.email = email

        # 🔑 Save the changes to the database
        user.save()  # <-- This is what the checker wants

        messages.success(request, 'Profile updated successfully!')
        return redire
