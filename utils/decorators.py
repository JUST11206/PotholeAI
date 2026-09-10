from functools import wraps

from flask import session, redirect, url_for


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return redirect(
                url_for("auth.login")
            )

        return function(*args, **kwargs)

    return wrapper


def role_required(role):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:

                return redirect(
                    url_for("auth.login")
                )

            if session.get("role") != role:

                return "Access Denied", 403

            return function(*args, **kwargs)

        return wrapper

    return decorator