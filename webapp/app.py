from flask import Flask, request, jsonify, render_template
from loquax import Document
from loquax.languages import Latin

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route("/loquax", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        text = data["text"]
        with_scansion = data.get("with_scansion", False)
        with_ipa = data.get("with_ipa", False)

        translation = Document(text, Latin, 75).to_string(ipa=with_ipa, scansion=with_scansion)

        return jsonify({"translation": translation})

    return render_template("index.html")
