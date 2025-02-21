import re
import urllib.parse
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_gpt_output():
    # Retrieve input from JSON or form-data.
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # Get the raw text from the request.
    raw_text = data.get("text", "").strip()
    processed_text = raw_text.strip()

    # Use regex to search for a mailto link that may include a query string.
    # The regex captures anything that starts with "mailto:" followed by non-space characters,
    # and optionally a '?' with additional characters.
    mailto_match = re.search(r'(mailto:[^\s"\'<>]+(?:\?[^\s"\'<>]+)?)', processed_text, re.IGNORECASE)
    
    if mailto_match:
        mailto_link_raw = mailto_match.group(1)
        # Split the link into the base (e.g., "mailto:someone@example.com")
        # and the query part (e.g., "subject=...&body=...").
        parts = mailto_link_raw.split('?', 1)
        base = parts[0]
        
        if len(parts) > 1:
            query = parts[1]
            # Parse the query parameters into a list of key-value pairs.
            query_list = urllib.parse.parse_qsl(query, keep_blank_values=True)
            # Re-encode the query parameters so that all special characters are percent‑encoded.
            # Using quote_via=urllib.parse.quote ensures spaces become %20 instead of '+'.
            encoded_query = urllib.parse.urlencode(query_list, quote_via=urllib.parse.quote)
            mailto_link = f"{base}?{encoded_query}"
        else:
            mailto_link = base

        # Create an HTML anchor tag with the properly encoded mailto link.
        html_link = f'<a href="{mailto_link}">Click here to send the email</a>'
    else:
        # If no mailto link is found, simply return the processed text.
        html_link = processed_text

    # Build the final HTML content.
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
    # Return the HTML page with the correct MIME type.
    return Response(html_content, mimetype='text/html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
