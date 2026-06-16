from streamlit_cookies_manager import EncryptedCookieManager

_cookies = None

def get_cookies():
    global _cookies

    if _cookies is None:
        _cookies = EncryptedCookieManager(
            prefix="pestly_",
            password="password-rahasia-kamu"
        )

    return _cookies