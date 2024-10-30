from django.shortcuts import render


def user_preferences(request):
    """Renders the main preferences page for a user"""
    context = {"page_title": "User preferences"}
    return render(request, "htmx/user/preferences.html", context=context)
