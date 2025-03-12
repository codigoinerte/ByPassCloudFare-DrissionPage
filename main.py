from urllib.parse import urlparse
from flask import Flask, request, jsonify
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions
import os
import re

# Chromium options arguments
arguments = [
    "-no-first-run",
    "-force-color-profile=srgb",
    "-metrics-recording-only",
    "-password-store=basic",
    "-use-mock-keychain",
    "-export-tagged-pdf",
    "-no-default-browser-check",
    "-disable-background-mode",
    "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
    "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
    "-deny-permission-prompts",
    "-disable-gpu",
    "-accept-lang=en-US",
    "--no-sandbox",  # Necessary for Docker
]

browser_path = "/usr/bin/google-chrome"
app = Flask(__name__)

# Function to check if the URL is safe
def is_safe_url(url: str) -> bool:
    parsed_url = urlparse(url)
    ip_pattern = re.compile(
        r"^(127\.0\.0\.1|localhost|0\.0\.0\.0|::1|10\.\d+\.\d+\.\d+|172\.1[6-9]\.\d+\.\d+|172\.2[0-9]\.\d+\.\d+|172\.3[0-1]\.\d+\.\d+|192\.168\.\d+\.\d+)$"
    )
    hostname = parsed_url.hostname
    if (hostname and ip_pattern.match(hostname)) or parsed_url.scheme == "file":
        return False
    return True

# Function to bypass Cloudflare protection
def bypass_cloudflare(url: str, retries: int, log: bool, proxy: str = None) -> ChromiumPage:
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path).headless(False)
    
    for arg in arguments:
        options.set_argument(arg)
        
    if proxy:
        options.set_proxy(proxy)
    
    options.set_argument("--auto-open-devtools-for-tabs", "true")
    options.set_argument("--remote-debugging-port=9222")
    options.set_argument("--no-sandbox")  # Necessary for Docker
    options.set_argument("--disable-gpu")
    options.set_argument("--headless", "new")
    
    driver = ChromiumPage(addr_or_opts=options)
    try:
        driver.get(url)
        cf_bypasser = CloudflareBypasser(driver, retries, log)
        cf_bypasser.bypass()
        return driver
    except Exception as e:
        driver.quit()
        raise e
    
# Endpoint to get the page source
@app.route('/get_page_source', methods=['POST'])
def get_page_source():
    data = request.get_json()
    url = data.get('url')
    retries = data.get('retries') or 5
    proxy = data.get('proxy') or None
    log = data.get('log') or False

    if not is_safe_url(url):
        return jsonify({"error": "URL is required"}), 400

    try:
        driver = bypass_cloudflare(url, retries, log, proxy)
        html = driver.html
        
        driver.quit()

        return jsonify({"data": html, "headless": "true"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)