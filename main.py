from flask import Flask, request, Response, render_template_string
import re

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_gpt_output():
    """
    Expects the GPT output to be passed as a parameter named 'text'
    in either form-data or JSON.

    Example input (JSON):
      {
         "text": "📧mailto:example@example.com?subject=Meeting%20Request&body=Dear%20John,..."
      }
    """
    # Get text from request (either form or JSON)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    raw_text = data.get("text", "").strip()

    # Remove any leading emoji or unwanted characters (like the mail icon)
    processed_text = raw_text.lstrip("📧").strip()

    # Check if "mailto:" appears anywhere in the text (case-insensitive)
    if "mailto:" in processed_text.lower():
        # Find the index of "mailto:" in a case-insensitive way
        lower_text = processed_text.lower()
        index = lower_text.find("mailto:")
        mailto_link = processed_text[index:]
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
    # Return the HTML content with the MIME type set to text/html
    return Response(html_content, mimetype='text/html')

if __name__ == "__main__":
    # For local testing (Railway will provide its own PORT)
    app.run(host="0.0.0.0", port=8080)
