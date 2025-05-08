from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/fb-thumbnail")
def get_fb_thumbnail():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "Please enable JavaScript" in resp.text or resp.status_code != 200:
            return jsonify({"error": "Cannot fetch page. Possibly requires login."}), 403

        soup = BeautifulSoup(resp.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image:
            return og_image["content"]
        else:
            return jsonify({"error": "og:image not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def hello():
    return "FB Thumbnail Scraper is running."
