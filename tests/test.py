import time
from os import getcwd, path
from unittest import TestCase, main

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By


class Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()

    def setUp(self):
        self.browser.get(path.join(getcwd(), "index.html"))

    def tearDown(self):
        _ = self.browser.get_log("browser")
        self.browser.get("about:blank")

    def test_no_errors(self):
        log = self.browser.get_log("browser")
        for message in log:
            self.assertNotEqual(message["level"], "SEVERE")

    def test_company_name_present(self):
        self.assertIn("Florist Blåklinten", self.browser.page_source)

    def test_footer(self):
        self.browser.find_element(By.TAG_NAME, "footer")

    def scroll_to_bottom(self):
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    def test_instagram_link(self):
        self.scroll_to_bottom()
        self.browser.find_element(By.ID, "instagram-link").click()
        self.assertEqual(
            "https://www.instagram.com/ntiuppsala/", self.browser.current_url
        )

    def test_twitter_link(self):
        self.scroll_to_bottom()
        self.browser.find_element(By.ID, "x-link").click()
        self.assertIn("https://twitter.com", self.browser.current_url)
        self.assertIn("ntiuppsala", self.browser.current_url)

    def test_facebook_link(self):
        self.scroll_to_bottom()
        self.browser.find_element(By.ID, "facebook-link").click()
        self.assertEqual(
            "https://www.facebook.com/ntiuppsala", self.browser.current_url
        )

    def test_phone_number_present(self):
        phone_number_links = self.browser.find_elements(
            By.XPATH, "//a[@href='tel:0630-555-555']"
        )
        for phone_number_link in phone_number_links:
            self.assertIn("0630-555-555", phone_number_link.text)

    def test_email_address_present(self):
        email_address_links = self.browser.find_elements(
            By.XPATH, "//a[@href='mailto:info@ntig-uppsala.github.io']"
        )
        for email_address_link in email_address_links:
            self.assertIn("info@ntig-uppsala.github.io", email_address_link.text)

    def test_address_present(self):
        self.assertIn("Fjällgatan 32H", self.browser.page_source)
        self.assertIn("981 39 Kiruna", self.browser.page_source)

    def test_opening_hours_present(self):
        self.assertIn("Öppettider", self.browser.page_source)
        self.assertIn("Måndag-fredag 10:00-16:00", self.browser.page_source)
        self.assertIn("Lördag 12:00-15:00", self.browser.page_source)

    def test_closed_days_present(self):
        closed_days = [
            ("Nyårsdagen", "1/1"),
            ("Trettondedag jul", "6/1"),
            ("Första maj", "1/5"),
            ("Sveriges nationaldag", "6/6"),
            ("Julafton", "24/12"),
            ("Juldagen", "25/12"),
            ("Annandag jul", "26/12"),
            ("Nyårsafton", "31/12"),
        ]
        self.assertIn("Stängda dagar", self.browser.page_source)

        opening_hour_list = self.browser.find_element(By.ID, "opening-hours")
        for closed_day in closed_days:
            self.assertIn(closed_day[0], opening_hour_list.text)
            self.assertIn(closed_day[1], opening_hour_list.text)

    def test_fonts(self):
        h1_font = self.browser.find_element(By.CLASS_NAME, "h1")
        self.assertEqual(
            h1_font.value_of_css_property("font-family"), '"DM Serif Display"'
        )
        p_fonts = self.browser.find_elements(By.TAG_NAME, "p")
        for p_font in p_fonts:
            self.assertEqual(p_font.value_of_css_property("font-family"), "Assistant")

    def test_favicon(self):
        self.browser.find_element(By.XPATH, ".//link[@rel='shortcut icon']")

    def test_logo(self):
        src = self.browser.find_element(
            By.XPATH, "//a[@class='navbar-brand']/img"
        ).get_attribute("src")
        self.assertIn(".svg", src)

    def test_navbar_mobile(self):
        self.browser.set_window_size(600, 600)

        try:
            nav_links = self.browser.find_elements(By.CLASS_NAME, "nav-link")
            for nav_link in nav_links:
                nav_link.click()

            self.fail(msg="Nav link is clickable")
        except ElementNotInteractableException:
            pass

        toggler = self.browser.find_element(By.CLASS_NAME, "navbar-toggler")
        toggler.click()

        nav_links = self.browser.find_elements(By.CLASS_NAME, "nav-link")
        for nav_link in nav_links:
            nav_link.click()

    def test_navbar_dektop(self):
        self.browser.set_window_size(1200, 600)

        nav_links = self.browser.find_elements(By.CLASS_NAME, "nav-link")
        for nav_link in nav_links:
            nav_link.click()

        try:
            toggler = self.browser.find_element(By.CLASS_NAME, "navbar-toggler")
            toggler.click()

            self.fail(msg="Navbar toggler is clickable")
        except ElementNotInteractableException:
            pass


if __name__ == "__main__":
    main(verbosity=2)
