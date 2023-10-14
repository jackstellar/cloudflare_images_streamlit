import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

# Cloudflare API details
API_TOKEN = "ogLef6Hjkaep_GUBJekTY7Re6QYw-_p5otHqyC_C"  # Replace with your Cloudflare API token
ACCOUNT_ID = "a9eb62809a84081e8eb1cc2d527231c8"  # Replace with your Cloudflare account ID

# Cloudflare Images API endpoint
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/images/v1"

# Fetch images using Cloudflare API
def fetch_images(page_number, per_page):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "page": page_number,
        "per_page": per_page
    }

    response = requests.get(API_BASE_URL, headers=headers, params=params)
    data = response.json()

    return data

# Display images in the Streamlit app
# Display images in the Streamlit app
def display_images(images):
    num_columns = 3  # Define the number of columns in the grid layout
    col_list = st.columns(num_columns)
    for image in images:
        try:
            if 'url' in image:
                col_idx = 0
                for col in col_list:
                    with col:
                        st.image(image['url'], use_column_width=True)
                        col_idx += 1
                        if col_idx >= num_columns:
                            break
            else:
                st.write(f"Image details not found for ID: {image.get('id', 'N/A')}")
        except Exception as e:
            st.write(f"Error displaying image with ID {image.get('id', 'N/A')}: {e}")


# Streamlit app layout
def main():
    # Initialize page_number and per_page
    page_number = 1
    per_page = 12

    st.header("Upload to Cloudflare Images")

    # ... (Your previous code)

    st.header("Cloudflare Images Gallery")
    # Fetch images using Cloudflare API
    response = fetch_images(page_number, per_page)
    images = response.get("result", {}).get("images", [])

    if not images:
        st.write("No images found.")
    else:
        st.write("Displaying {} images:".format(len(images)))
        display_images(images)

# Upload image using Cloudflare API
# ... (Your previous code)

if __name__ == "__main__":
    main()
