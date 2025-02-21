import re
import urllib.parse
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_gpt_output():
    # Get text from request (either form or JSON)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    raw_text = data.get("text", "").strip()
    processed_text = raw_text.strip()

    # Use regex to search for a mailto link that might include query parameters
    mailto_match = re.search(r'(mailto:[^\s"\'<>]+(?:\?[^\s"\'<>]+)?)', processed_text, re.IGNORECASE)
    if mailto_match:
        mailto_link_raw = mailto_match.group(1)
        # Split the mailto link into its base part and query part
        parts = mailto_link_raw.split('?', 1)
        base = parts[0]  # e.g., "mailto:john@example.com"
        if len(parts) > 1:
            query = parts[1]  # e.g., "subject=Meeting&body=Hello John, let's talk soon!"
            # Process each query parameter: split by '&', then '='
            query_params = {}
            for param in query.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    # Re-encode the value to ensure spaces and special characters are URL-safe
                    query_params[k] = urllib.parse.quote(v, safe='')
            # Build the properly encoded query string
            encoded_query = urllib.parse.urlencode(query_params)
            mailto_link = f"{base}?{encoded_query}"
        else:
            mailto_link = base

        # Create the clickable HTML anchor tag
        html_link = f'<a href="{mailto_link}">Click here to send the email</a>'
    else:
        # If no mailto link is found, simply use the processed text
        html_link = processed_text

    # Create a full HTML page with the clickable link
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
