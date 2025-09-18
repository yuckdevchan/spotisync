from playwright.sync_api import Browser, sync_playwright
from dotenv import load_dotenv
from os import environ as env
import json

load_dotenv()

def get_context(browser: Browser):
    return browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        device_scale_factor=1,
        is_mobile=False,
        locale="en-US"
    )

def login_to_spotify(email: str, password: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--enable-widevine-cdm"])
        context = get_context(browser)
        page = context.new_page()
        page.goto("https://accounts.spotify.com/en/login")
        page.fill("input#login-username", email)
        page.click("button#login-button")
        page.wait_for_timeout(2000)
        # Check for both 'with a password' and 'without a password' buttons
        with_password_selector = "button[data-encore-id='buttonTertiary']"
        without_password_selector = "button[data-encore-id='buttonTertiary'][data-testid='web-player-link']"
        if page.query_selector(with_password_selector):
            page.click(with_password_selector)
            page.fill("input#login-password", password)
            page.click("button#login-button")
        elif page.query_selector(without_password_selector):
            page.click(without_password_selector)
        # Accept cookies if present
        if page.query_selector("button#onetrust-accept-btn-handler"):
            page.click("button#onetrust-accept-btn-handler")
        page.wait_for_load_state("networkidle")
        context.storage_state(path="spotify_cookies.json")
        browser.close()

def play_song_on_spotify(id: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--enable-widevine-cdm"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            device_scale_factor=1,
            is_mobile=False,
            locale="en-US",
            storage_state="spotify_cookies.json"
        )
        page = context.new_page()
        page.goto(f"https://open.spotify.com/track/{id}")
        page.wait_for_timeout(99999999)

# login_to_spotify(env["SPOTIFY_EMAIL"], env["SPOTIFY_PASSWORD"])
play_song_on_spotify("0hMvI4iye2BtqOPL57qfya")
