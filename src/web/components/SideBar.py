from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class SideBar:

    def __init__(self, page: Page):
        self.page = page

        self._menu = page.locator('.mainnav-menu')

        self._logo = page.locator("button.btn-open")
        self._close_button = page.get_by_role('button', name='Close')

        self._tests_link = page.get_by_role('link', name='Tests')
        self._runs_link = page.get_by_role('link', name='Runs')
        self._plans_link = page.get_by_role('link', name='Plans')
        self._steps_link = page.get_by_role('link', name='Steps')
        self._pulse_link = page.get_by_role('link', name='Pulse')
        self._imports_link = page.get_by_role('link', name='Imports')
        self._analytics_link = page.get_by_role('link', name='Analytics')
        self._branches_link = page.get_by_role('link', name='Branches')
        self._settings_link = page.get_by_role('link', name='Settings')

        self._help_link = page.get_by_role('link', name='Help')
        self._projects_link = page.get_by_role('link', name='Projects')

    def is_loaded(self) -> SideBar:
        expect(self._menu).to_be_visible()
        expect(self._logo).to_be_visible()
        expect(self._projects_link).to_be_visible()
        return self

    def go_to_tests(self) -> SideBar:
        self._tests_link.click()
        return self

    def go_to_runs(self) -> SideBar:
        self._runs_link.click()
        return self

    def go_to_plans(self) -> SideBar:
        self._plans_link.click()
        return self

    def go_to_steps(self) -> SideBar:
        self._steps_link.click()
        return self

    def go_to_pulse(self) -> SideBar:
        self._pulse_link.click()
        return self

    def go_to_imports(self) -> SideBar:
        self._imports_link.click()
        return self

    def go_to_analytics(self) -> SideBar:
        self._analytics_link.click()
        return self

    def go_to_branches(self) -> SideBar:
        self._branches_link.click()
        return self

    def go_to_settings(self) -> SideBar:
        self._settings_link.click()
        return self

    def go_to_help(self) -> SideBar:
        self._help_link.click()
        return self

    def go_to_projects(self) -> SideBar:
        self._projects_link.click()
        return self

    def click_logo(self) -> SideBar:
        self._logo.click()
        return self

    def close_menu(self) -> SideBar:
        self._close_button.click()
        return self

    def get_user_profile_link(self, user_name: str):
        return self.page.get_by_role('link', name=user_name)

    def click_user_profile(self, user_name: str) -> SideBar:
        self.get_user_profile_link(user_name).click()
        return self

    def link_by_name(self, name: str):
        return self._menu.locator(f"a:has-text('{name}')")

    def expect_tab_active(self, name: str) -> SideBar:
        link = self.link_by_name(name)
        expect(link).to_be_visible()
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self
