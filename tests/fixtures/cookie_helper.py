from playwright.sync_api import BrowserContext, Cookie, Page


class CookieHelper:
    def __init__(self, context: BrowserContext):
        self.context = context  # Зберігаємо саме контекст

    def add(self, name: str, value: str, domain: str, **kwargs) -> None:
        """Adds a cookie to the browser context."""
        cookie: Cookie = {
            "name": name,
            "value": value,
            "domain": domain,
            "path": kwargs.get("path", "/"),
            "httpOnly": kwargs.get("http_only", False),
            "secure": kwargs.get("secure", False),
            "sameSite": kwargs.get("same_site", "Lax"),
        }
        if "expires" in kwargs:
            cookie["expires"] = kwargs["expires"]

        # Correctly call add_cookies on the stored context
        self.context.add_cookies([cookie])

    def add_many(self, cookies: list[Cookie]) -> None:
        """Add multiple cookies to the context."""
        self.context.add_cookies(cookies)

    def get_all(self, urls: list[str] | None = None) -> list[Cookie]:
        """Get all cookies, optionally filtered by URLs."""
        return self.context.cookies(urls) if urls else self.context.cookies()

    def get(self, name: str) -> Cookie | None:
        """Get a specific cookie by name."""
        for cookie in self.context.cookies():
            if cookie["name"] == name:
                return cookie
        return None

    def get_value(self, name: str) -> str | None:
        """Get the value of a specific cookie."""
        cookie = self.get(name)
        return cookie["value"] if cookie else None

    def exists(self, name: str) -> bool:
        """Check if a cookie exists."""
        return self.get(name) is not None

    def clear_all(self) -> None:
        """Clear all cookies."""
        self.context.clear_cookies()

    def clear(self, *, name: str | None = None, domain: str | None = None, path: str | None = None):
        """Clear cookies matching the specified criteria."""
        self.context.clear_cookies(name=name, domain=domain, path=path)

    @staticmethod
    def clear_browser_state(page: Page) -> None:
        """Clear browser state including cookies, localStorage, and sessionStorage."""
        page.context.clear_cookies()
        page.evaluate("window.localStorage.clear();")
        page.evaluate("window.sessionStorage.clear();")
