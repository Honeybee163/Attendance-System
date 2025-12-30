# your_app/decorators.py
from django.shortcuts import redirect
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                profile = getattr(request.user, 'studentprofile', None)
                if profile and profile.role == role:
                    return view_func(request, *args, **kwargs)
            return redirect('login')  # or an unauthorized page
        return _wrapped_view
    return decorator
