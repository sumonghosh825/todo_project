from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Task

CustomUser = get_user_model()


# **User Registration (Plain-Text Password)**
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        # Manually creating user without password hashing
        user = CustomUser(username=username, email=email)
        user.password = password  # Storing password as plain text
        user.save()  # Save user to database

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, "authentication/register.html")

# **User Login (Username or Email)**
def user_login(request):
    if request.method == "POST":
        login_input = request.POST.get('login_input')  # Can be username or email
        password = request.POST.get('password')

        # Find user by username or email
        user = CustomUser.objects.filter(username=login_input).first() or \
               CustomUser.objects.filter(email=login_input).first()

        if user and user.password == password:  # Manual password check (INSECURE)
            login(request, user)  # Log in user
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password!")

    return render(request, "authentication/login.html")


# **User Logout**
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# **Home Page**
@login_required
def home(request):
    return render(request, 'index.html', {'username': request.user.username})


# **Task Management**
@login_required
def task_management(request):
    query = request.GET.get('search', '')
    tasks = Task.objects.filter(name__icontains=query, assigned_by=request.user) if query else Task.objects.filter(assigned_by=request.user)
    
    return render(request, 'task.html', {'tasks': tasks})


@login_required
def load_tasks_by_category(request, category):
    tasks = Task.objects.filter(category=category, assigned_by=request.user)
    return render(request, "task_catagory.html", {"tasks": tasks, "task_category": category})

@login_required
def load_tasks_by_status(request, status):
    tasks = Task.objects.filter(status=status, assigned_by=request.user)
    return render(request, "task_status.html", {"tasks": tasks, "task_status": status})



@login_required
def add_task(request):
    if request.method == "POST":
        name = request.POST.get('name')
        time_period = request.POST.get('time_period')
        category = request.POST.get('category', 'Personal')  # Default to Personal
        priority = request.POST.get('priority', 1)  # Default priority is 1 (Low)
        status = request.POST.get('status', 'Pending')  # Default status is Pending

        Task.objects.create(
            name=name,
            time_period=time_period,
            category=category,
            priority=int(priority),
            status=status,
            assigned_by=request.user
        )

        messages.success(request, "Task added successfully!")
        return redirect('task_management')

    return JsonResponse({'error': 'Invalid Request'}, status=400)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_by=request.user)

    if request.method == "POST":
        task.name = request.POST.get("name", task.name)
        task.time_period = request.POST.get("time_period", task.time_period)
        task.category = request.POST.get("category", task.category)
        task.priority = int(request.POST.get("priority", task.priority))
        task.status = request.POST.get("status", task.status)

        task.save()
        messages.success(request, "Task updated successfully!")
        return redirect('task_management')

    return JsonResponse({"success": False}, status=400)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_by=request.user)

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)


# **Profile View**
@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def load_profile_content(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = profile(request.POST, instance=profile)
        if form.is_valid():
            profile.save()
            return JsonResponse({"status": "success"})
        
        return JsonResponse({"status": "error", "errors": form.errors})
    
    return render(request, "profile_modal.html", {"profile": profile})


@login_required
def update_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name", profile.full_name)
        profile.phone_number = request.POST.get("phone_number", profile.phone_number)
        profile.gender = request.POST.get("gender", profile.gender)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.hobbies = request.POST.get("hobbies", profile.hobbies)
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "profile.html", {"profile": profile})


# **Security Settings**
@login_required
def load_security_content(request):
    return render(request, "security_modal.html", {"user": request.user})

@login_required
def update_security(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Validate password match
        if new_password and new_password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match."})

        user = request.user

        # Update email if changed
        if email and email != user.email:
            if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({"status": "error", "message": "Email already in use."})
            user.email = email

        # Update password (Plain text, as per register function)
        if new_password:
            user.password = new_password  # Storing password as plain text (INSECURE)
        
        user.save()
        return redirect('login')

    return redirect('profile')
