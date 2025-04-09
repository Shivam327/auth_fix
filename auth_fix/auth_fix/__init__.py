# custom_app/__init__.py

import frappe
from frappe import local
from frappe.auth import CookieManager


def patched_set_cookie(
    self,
    key,
    value,
    expires=None,
    secure=False,
    httponly=False,
    samesite="Lax",
    max_age=None,
):
    secure = True
    httponly = True

    if not secure and hasattr(local, "request"):
        secure = local.request.scheme == "https"

    self.cookies[key] = {
        "value": value,
        "expires": expires,
        "secure": secure,
        "httponly": httponly,
        "samesite": samesite,
        "max_age": max_age,
    }


def apply_cookie_patch():
    if not getattr(frappe, "_custom_cookie_patched", False):
        CookieManager.set_cookie = patched_set_cookie
        frappe._custom_cookie_patched = True


# ✅ Apply patch immediately
apply_cookie_patch()
