from flask import Flask, request, Response
import re

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_gpt_output():
    # Get text from request (either form or JSON)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    raw_text = data.get("text", "").strip()

    # Check if the raw text starts with the email icon; if so, remove it.
    if raw_text.startswith("📧"):
        processed_text = raw_text.lstrip("📧").strip()
    else:
        processed_text = raw_text.strip()

    # Use a regex to search for a mailto link more robustly
    mailto_match = re.search(r'(mailto:[^\s"\'<>]+)', processed_text, re.IGNORECASE)
    if mailto_match:
        mailto_link = mailto_match.group(1)
        html_link = f'<a href="{mailto_link}">Click here to send the email</a>'
    else:
        html_link = processed_text

    # Create a full HTML page containing the clickable email link
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Processed Email Link</title>
</head>
<body>
  {html_link}
</body>
</html>
"""
    return Response(html_content, mimetype='text/html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
