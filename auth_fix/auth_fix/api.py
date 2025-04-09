import base64
from Crypto.Cipher import AES
import frappe
from frappe.auth import LoginManager

BS = 16


def unpad(s):
    try:
        pad_len = ord(s[-1:])
        return s[:-pad_len]
    except Exception as e:
        raise ValueError("Invalid padding")


def decrypt_password(encrypted_text, key_str):
    try:
        key = key_str.encode("utf-8")
        encrypted = base64.b64decode(encrypted_text)

        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted)

        unpadded = unpad(decrypted)

        decrypted_text = unpadded.decode("utf-8")

        return decrypted_text
    except Exception as e:
        error_msg = f"Decryption failed: {str(e)}"
        frappe.log_error(frappe.get_traceback(), "SecureLogin: Decryption Error")
        raise frappe.ValidationError(error_msg)


@frappe.whitelist(allow_guest=True)
def secure_login(usr, pwd):
    try:

        decrypted_pwd = decrypt_password(pwd, "mysecurekey12345")

        login_manager = LoginManager()
        login_manager.authenticate(user=usr, pwd=decrypted_pwd)
        login_manager.post_login()

        frappe.local.response["message"] = "Logged In"

    except frappe.AuthenticationError as e:
        msg = f"Authentication failed for user '{usr}': {str(e)}"
        frappe.local.response["message"] = msg
        frappe.local.response["http_status_code"] = 401

    except frappe.ValidationError as e:
        msg = f"Validation error: {str(e)}"
        frappe.local.response["message"] = msg
        frappe.local.response["http_status_code"] = 417

    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        frappe.log_error(frappe.get_traceback(), "Secure Login Unexpected Error")
        frappe.local.response["message"] = msg
        frappe.local.response["http_status_code"] = 500
