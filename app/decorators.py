from functools import wraps

from flask import abort, request
from flask_login import current_user
from .utils.utils import get_user_api, verif_api_key


def permission_required(perm):
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if perm == "admin":
                if request.path.startswith("/api/"):
                    api_key = request.headers.get("X-API-KEY")
                    if not api_key:
                        abort(403)
                    user = get_user_api(api_key)
                    if not user or not user.is_admin():
                        abort(403)
                elif not current_user.is_admin():
                    abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def verification_required():
    """Restrict an api access to users without a key"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.path.startswith("/api/") and verif_api_key(request.headers):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required("admin")(f)

def api_required(f):
    return verification_required()(f)

