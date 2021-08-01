from pathlib import Path
from flask import Flask, render_template, jsonify, request, make_response
from .service import JournalService


def setup_routes(app: Flask):
    @app.get("/")
    def home():
        html = contents = Path("static/index.html").read_text()
        response = make_response(html, 200)
        response.mimetype = "text/html"
        return response

    @app.get("/search")
    def search():
        result = JournalService.search(request.args.get("q") or "*")
        return jsonify(result)

    @app.get("/articles/<id>")
    def get_article(id):
        result = JournalService.get_by_id(id)
        return jsonify(result)
