from streamlit_cookies_manager import EncryptedCookieManager

_cookies = None

def get_cookies():
    global _cookies

    if _cookies is None:
        _cookies = EncryptedCookieManager(
            prefix="pestly_",
            password="pestly-secret-key"
        )

    if not _cookies.ready():
        return None

    return _cookies