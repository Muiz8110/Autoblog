import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve WordPress credentials and site URL from environment variables
WP_SITE_URL = os.getenv("WP_SITE_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")  # This should be your Application Password

def upload_image_to_wordpress(image_path):
    """Upload an image to WordPress and return the media ID."""
    if not WP_SITE_URL or not WP_USERNAME or not WP_PASSWORD:
        return None, "WordPress credentials are missing!"

    # Open image in binary model
    try:
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
    except Exception as e:
        return None, f"Error reading the image file: {e}"

    api_url = f"{WP_SITE_URL}/wp-json/wp/v2/media"
    auth = HTTPBasicAuth(WP_USERNAME, WP_PASSWORD)

    # Upload the image
    response = requests.post(
        api_url,
        auth=auth,
        files={"file": (os.path.basename(image_path), img_data, "image/png")},
    )

    if response.status_code == 201:
        return response.json()["id"], "Image uploaded successfully!"
    else:
        return None, f"Failed to upload image: {response.status_code} - {response.text}"

def post_to_wordpress(title, content, image_path=None):
    """Publish generated content to WordPress with an optional featured image."""
    if not WP_SITE_URL or not WP_USERNAME or not WP_PASSWORD:
        return "WordPress credentials are missing!"

    api_url = f"{WP_SITE_URL}/wp-json/wp/v2/posts"
    auth = HTTPBasicAuth(WP_USERNAME, WP_PASSWORD)
    media_id = None

    # Upload image if provided
    if image_path:
        media_id, img_message = upload_image_to_wordpress(image_path)
        if not media_id:
            return img_message

    # Prepare post data
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
    }
    
    # Add the featured image if available
    if media_id:
        post_data["featured_media"] = media_id

    # Make the request to create the post
    try:
        response = requests.post(api_url, auth=auth, json=post_data)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Return success message with post ID
        return f"Post published successfully! ID: {response.json().get('id')}"
    
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} - {response.text}"
    except Exception as err:
        return f"An error occurred: {err}"

# Example usage
if __name__ == "__main__":
    title = "Test Post from API"
    content = "This is a test post created using the WordPress REST API."
    image_path = "path_to_your_image.png"  # Replace with your image path

    result = post_to_wordpress(title, content, image_path)
    print(result)