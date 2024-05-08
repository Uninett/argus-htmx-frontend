# Should probably be in a theming-app


DEFAULT_THEME = "default"


def theme_via_GET(request):
    theme = request.GET("theme", DEFAULT_THEME)
    return {"theme": theme}


def theme_via_session(request):
    theme = request.session.get("theme", DEFAULT_THEME)
    return {"theme": theme}
