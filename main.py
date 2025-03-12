# filepath: /var/www/cloudfare/main.py
from flask import Flask, request, jsonify
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions
import os

app = Flask(__name__)

@app.route('/get_page_source', methods=['POST'])
def get_page_source():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        co = ChromiumOptions()
        driver = ChromiumPage(addr_or_opts=co)
        driver.get(url)

        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()

        page_source = driver.html
        driver.quit()

        return jsonify({"data": page_source}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)