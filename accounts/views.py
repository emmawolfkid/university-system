from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

from .forms import StudentRegistrationForm


# 🔐 ROLE-BASED DECORATOR (SAFE VERSION)
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.role not in allowed_roles:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('login')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# 📝 STUDENT REGISTRATION
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Wait for admin approval.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# 🔐 LOGIN VIEW
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not user.is_approved:
                messages.error(request, "Account not approved yet.")
                return redirect('login')

            login(request, user)

            return redirect_user_dashboard(user)

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


# 🔁 CENTRAL REDIRECT LOGIC (VERY IMPORTANT)
def redirect_user_dashboard(user):
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'instructor':
        return redirect('instructor_dashboard')
    elif user.role == 'accountant':
        return redirect('accountant_dashboard')
    elif user.role == 'staff':
        return redirect('staff_dashboard')
    else:
        return redirect('admin_dashboard')


# 🚪 LOGOUT
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# 🎓 STUDENT DASHBOARD
@login_required
@role_required(['student'])
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')


# 👨‍🏫 INSTRUCTOR DASHBOARD
@login_required
@role_required(['instructor'])
def instructor_dashboard(request):
    return render(request, 'accounts/instructor_dashboard.html')


# 💰 ACCOUNTANT DASHBOARD
@login_required
@role_required(['accountant'])
def accountant_dashboard(request):
    return render(request, 'accounts/accountant_dashboard.html')


# 🧑‍💼 STAFF DASHBOARD (OTHER STAFF)
@login_required
@role_required(['staff'])
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')


# 👑 ADMIN DASHBOARD
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')