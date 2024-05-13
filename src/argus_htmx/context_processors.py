# Should probably be in a theming-app


def theme_via_GET(request):
    theme = request.GET.get("theme", None)
    return {"theme": theme}


def theme_via_session(request):
    theme = request.session.get("theme", None)
    return {"theme": theme}
