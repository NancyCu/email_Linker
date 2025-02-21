from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_gpt_output():
    """
    Expects the GPT output to be passed as a parameter named 'text'
    in either form-data or JSON.
    
    Example input:
      {
         "text": "📧mailto:transferarticulation@uta.edu?subject=RE:%20Assistance%20Needed%20with%20Math%20Credit%20for%20University%20Studies&body=Dear%20Belinda%20Autman,..."
      }
    """
    # Get text from request (either form or JSON)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    raw_text = data.get("text", "").strip()

    # Remove any leading emoji or unwanted characters
    processed_text = raw_text.lstrip("📧").strip()

    # Verify the text starts with "mailto:"
    if processed_text.startswith("mailto:"):
        # Create a clickable HTML link
        html_link = f'<a href="{processed_text}">Click here to send the email</a>'
    else:
        # If no valid mailto link found, just return the original text
        html_link = processed_text

    # Wrap in a basic HTML page
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
    return html_content

if __name__ == "__main__":
    # For Railway deployment, use the port assigned by environment variable if needed.
    # Here we use port 8080 for local testing.
    app.run(host="0.0.0.0", port=8080)
