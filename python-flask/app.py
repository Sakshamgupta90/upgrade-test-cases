import io
from datetime import date

from markupsafe import Markup
from flask import Flask, jsonify, request, send_file
from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


app = Flask(__name__)
app.json = CustomJSONProvider(app)
app.json.sort_keys = False

ITEMS = {}


def seed_items():
    ITEMS["1"] = {"name": "Widget", "added": date(2021, 5, 1)}
    ITEMS["2"] = {"name": "Gadget", "added": date(2021, 6, 12)}


seed_items()


@app.route("/items")
def list_items():
    return jsonify(ITEMS)


@app.route("/banner")
def banner():
    name = request.args.get("name", "guest")
    return Markup("<h1>Hello, %s</h1>") % name


@app.route("/export")
def export_items():
    rows = "id,name\n" + "".join(f"{k},{v['name']}\n" for k, v in ITEMS.items())
    return send_file(
        io.BytesIO(rows.encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="items.csv",
    )


if __name__ == "__main__":
    app.run(debug=True)
