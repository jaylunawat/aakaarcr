from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CRLoginForm, CRRegistrationForm, ContactMessageForm, ProfileForm, SubmissionForm
from .models import Submission, Task, TaskZero


def _leaderboard_rows(limit=30):
    """Produce one trustworthy ranking source for the homepage and full board."""
    profiles = TaskZero.objects.select_related("user").filter(user__is_active=True)
    profiles = profiles.annotate(total_points=Coalesce(Sum("user__submission__marks"), 0)).order_by(
        "-total_points", "user__date_joined", "id"
    )
    return [
        {"rank": rank, "profile": profile, "points": profile.total_points}
        for rank, profile in enumerate(profiles[:limit], start=1)
    ]


def home(request):
    return render(request, "site/index.html", {
        "registration_form": CRRegistrationForm(),
        "login_form": CRLoginForm(request=request),
        "leaderboard_rows": _leaderboard_rows(limit=5),
    })


def static_page(request, page):
    allowed_pages = {"about", "roles", "incentives", "faq", "team", "day"}
    if page not in allowed_pages:
        return redirect("home")
    return render(request, f"site/{page}.html")


def register_cr(request):
    if request.method != "POST":
        return redirect("home")
    form = CRRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your CR account has been created. Welcome to Aakaar '26.")
        return redirect("dashboard")
    messages.error(request, "Please correct the highlighted registration details.")
    return render(request, "site/index.html", {
        "registration_form": form,
        "login_form": CRLoginForm(request=request),
        "leaderboard_rows": _leaderboard_rows(limit=5),
        "show_register": True,
    }, status=400)


def user_login(request):
    if request.method != "POST":
        return redirect("home")
    form = CRLoginForm(request=request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Signed in successfully.")
        return redirect(request.POST.get("next") or "dashboard")
    messages.error(request, "We could not sign you in. Check your email and password.")
    return render(request, "site/index.html", {
        "registration_form": CRRegistrationForm(),
        "login_form": form,
        "leaderboard_rows": _leaderboard_rows(limit=5),
        "show_login": True,
    }, status=400)


def user_logout(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


@login_required
def dashboard(request):
    profile = get_object_or_404(TaskZero, user=request.user)
    points = Submission.objects.filter(user=request.user, graded=True).aggregate(total=Coalesce(Sum("marks"), 0))["total"]
    rows = _leaderboard_rows(limit=500)
    rank = next((row["rank"] for row in rows if row["profile"].id == profile.id), None)
    return render(request, "portal/dashboard.html", {
        "profile": profile,
        "points": points,
        "rank": rank,
        "recent_submissions": Submission.objects.filter(user=request.user).select_related("task")[:8],
        "profile_form": ProfileForm(instance=profile),
    })


@login_required
def update_profile(request):
    if request.method != "POST":
        return redirect("dashboard")
    profile = get_object_or_404(TaskZero, user=request.user)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
    else:
        messages.error(request, "Profile update failed. Check the submitted fields.")
    return redirect("dashboard")


@login_required
def tasks_page(request):
    active_tasks = Task.objects.filter(is_published=True).filter(
        deadline__isnull=True
    ) | Task.objects.filter(is_published=True, deadline__gte=timezone.now())
    active_tasks = active_tasks.order_by("sort_order", "-id")
    if request.method == "POST":
        task = get_object_or_404(active_tasks, id=request.POST.get("task_id"))
        existing = Submission.objects.filter(user=request.user, task=task).first()
        form = SubmissionForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.user = request.user
            submission.graded = False
            submission.marks = 0
            submission.save()
            messages.success(request, f"Your evidence for {task.title} is now in the review queue.")
        else:
            messages.error(request, "Add a public evidence link or file before submitting.")
        return redirect("tasks_page")
    submissions = {item.task_id: item for item in Submission.objects.filter(user=request.user, task__in=active_tasks).select_related("task")}
    return render(request, "portal/tasks.html", {"tasks": active_tasks, "submissions": submissions, "submission_form": SubmissionForm()})


def leaderboard(request):
    return render(request, "portal/leaderboard.html", {"leaderboard_rows": _leaderboard_rows()})


def contact(request):
    if request.method != "POST":
        return redirect("team_page")
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Your message has reached the Aakaar CR team. We will reply using your email.")
    else:
        messages.error(request, "Please complete your name, email, subject, and message.")
    return redirect("team_page")


class PortalPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.txt"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")


class PortalPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class PortalPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PortalPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
