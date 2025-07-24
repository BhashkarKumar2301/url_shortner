from flask import Flask, request, jsonify, redirect, abort
from app.models import URLStore
from app.utils import generate_short_code, is_valid_url
from datetime import datetime

app = Flask(__name__)
url_store = URLStore()

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok"})

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data['url']

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while url_store.exists(short_code):
        short_code = generate_short_code()

    url_store.save_url(short_code, original_url)

    return jsonify({
        "short_code": short_code,
        "original_url": original_url,
        "short_url": request.host_url + short_code,
        "created_at": url_store.get_url_data(short_code)['created_at']
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_data = url_store.get_url_data(short_code)
    if url_data:
        url_store.increment_clicks(short_code)
        return redirect(url_data['url'])
    return jsonify({"error": "Short URL not found"}), 404

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    url_data = url_store.get_url_data(short_code)
    if not url_data:
        return jsonify({"error": "Short URL not found"}), 404
    return jsonify({
        "url": url_data['url'],
        "clicks": url_data['clicks'],
        "created_at": url_data['created_at']
    })

print(app.url_map)