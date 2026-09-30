from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ContactMessage, Submission, Task, TaskZero


class CRPortalFlowTests(TestCase):
    def test_registration_creates_account_and_profile(self):
        response = self.client.post(reverse("register_cr"), {
            "full_name": "Aarav Sharma",
            "email": "aarav@example.edu",
            "phone": "9999999999",
            "college": "Demo Institute",
            "academic_year": "3rd Year (UG)",
            "password1": "safe-password-123",
            "password2": "safe-password-123",
        })
        self.assertRedirects(response, reverse("dashboard"))
        user = get_user_model().objects.get(username="aarav@example.edu")
        self.assertEqual(user.cr_profile.crid, f"AK26{user.id:05d}")

    def test_submission_is_queued_and_awarded_points_feed_leaderboard(self):
        user = get_user_model().objects.create_user("cr@example.edu", password="safe-password-123")
        TaskZero.objects.create(
            user=user, crid="AK2600001", names="Campus Rep", username=user.username,
            email=user.username, emails=user.username, colgName="Demo Institute", state="", city="",
            mobileNo="9999999999", dept="", whatsappNo="9999999999", pincode="", address="",
        )
        task = Task.objects.create(title="Outreach", description="Share the update.", points=50, deadline=timezone.now() + timedelta(days=3))
        self.client.force_login(user)
        response = self.client.post(reverse("tasks_page"), {"task_id": task.id, "link": "https://example.com/proof"})
        self.assertRedirects(response, reverse("tasks_page"))
        submission = Submission.objects.get(task=task, user=user)
        self.assertFalse(submission.graded)
        submission.marks, submission.graded = 50, True
        submission.save()
        response = self.client.get(reverse("leaderboard"))
        self.assertContains(response, "Campus Rep")
        self.assertContains(response, "50 XP")

    def test_contact_message_is_saved(self):
        response = self.client.post(reverse("contact"), {
            "name": "Aarav", "email": "aarav@example.edu", "subject": "Support", "message": "Please help.",
        })
        self.assertRedirects(response, reverse("team_page"))
        self.assertEqual(ContactMessage.objects.count(), 1)
