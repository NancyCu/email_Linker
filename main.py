import re
from flask import Flask, request, Response, redirect, url_for

app = Flask(__name__)

# 1. This route handles both typed text and image uploads
@app.route("/submit", methods=["POST"])
def submit_text_or_image():
    """
    Unified endpoint:
      - If user uploads an image, we pretend to do OCR (placeholder).
      - If user types or pastes text, we use that directly.
      - We detect an email address and build a mailto link if found.
      - Finally, we return clickable HTML.
    """

    # -------------------------------
    # STEP 1: Extract input (text or image)
    # -------------------------------
    typed_text = request.form.get("text", "")  # Text from a form input
    uploaded_file = request.files.get("file")  # Image file from <input type="file">

    # Mocked extracted text (OCR placeholder)
    extracted_text = ""

    if uploaded_file:
        # In reality, you'd do actual OCR here
        # For demonstration, we pretend the OCR found some text:
        extracted_text = "Hello, I'd like to borrow money. Email me at johndoe@example.com"
    else:
        # No image, so we rely on typed text
        extracted_text = typed_text.strip()

    # -------------------------------
    # STEP 2: Build a final string that GPT might generate
    # (For demonstration, we just show "extracted_text" + a possible GPT response.)
    # -------------------------------
    # In your real setup, this is where your GPT logic would run,
    # possibly returning a text that includes "📧mailto:...".
    # We'll do a simpler approach: detect an email & build a mailto link ourselves.
    gpt_like_output = generate_gpt_response_with_mailto(extracted_text)

    # -------------------------------
    # STEP 3: Pass the GPT-like output to a "post-process" step
    # -------------------------------
    final_html = post_process_to_clickable_link(gpt_like_output)

    return Response(final_html, mimetype='text/html')


def generate_gpt_response_with_mailto(raw_text: str) -> str:
    """
    Simulate GPT logic: If an email is found, build a mailto link.
    Otherwise, just return the text.
    """
    # Detect an email address in the raw text
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
    if email_match:
        email = email_match.group(0)
        # For demonstration, we add a subject & body
        subject = "Quick%20Favor"
        body = "Hello,%0A%0AI wanted to follow up on your request.%0A%0AThanks!"
        mailto_link = f"📧mailto:{email}?subject={subject}&body={body}"

        # Combine the raw text with a "📧mailto:" style link (the way your GPT might do)
        return f"{raw_text}\n\nHere is your link:\n{mailto_link}"
    else:
        # If no email is found, we can still return the raw text
        return raw_text


def post_process_to_clickable_link(gpt_text: str) -> str:
    """
    This function mimics your existing /process endpoint logic:
    - Looks for "📧mailto:" in the GPT text.
    - If found, convert to a clickable <a> tag.
    - Return a full HTML page with the final link.
    """

    # Remove leading 📧 if present at the start
    # (But let's do a more robust approach with regex.)
    processed_text = gpt_text.strip()

    # Regex to find any 'mailto:' link
    mailto_match = re.search(r'(mailto:[^\s"\'<>]+)', processed_text, re.IGNORECASE)
    if mailto_match:
        mailto_link = mailto_match.group(1)
        # Build an HTML anchor
        anchor_tag = f'<a href="{mailto_link}">Click here to send the email</a>'
        # Replace the mailto portion in the text with the anchor tag
        # Or you can just append it at the bottom.
        # For clarity, let's do a simple replacement:
        final_text = re.sub(r'(📧mailto:[^\s"\'<>]+)', anchor_tag, processed_text, flags=re.IGNORECASE)
    else:
        final_text = processed_text

    # Wrap in basic HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Final Output</title>
</head>
<body>
  <p>{final_text.replace('\n', '<br>')}</p>
</body>
</html>
"""
    return html_content


if __name__ == "__main__":
    # Run locally on port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)
