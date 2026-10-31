
from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from io import BytesIO
import base64

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    qr_data = None
    entered_text = ""

    if request.method == "POST":
        entered_text = request.form.get("text", "").strip()

        if entered_text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=ERROR_CORRECT_H,
                box_size=10,
                border=4
            )

            qr.add_data(entered_text)
            qr.make(fit=True)

            image = qr.make_image(
                fill_color="black",
                back_color="white"
            )

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            qr_data = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

    return render_template(
        "generate.html",
        qr_data=qr_data,
        entered_text=entered_text
    )


@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("text", "").strip()

    if not text:
        return "Please enter some text first.", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(text)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="QRGen.png"
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=False)
