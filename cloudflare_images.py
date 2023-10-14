import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

# Cloudflare API details
API_TOKEN = "ogLef6Hjkaep_GUBJekTY7Re6QYw-_p5otHqyC_C"
ACCOUNT_ID = "a9eb62809a84081e8eb1cc2d527231c8"

# Cloudflare Images API endpoint
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/images/v1"

# Streamlit app layout
def main():
    st.header("Upload to Cloudflare Images")

    # Image uploader
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        metadata = st.text_input("Image Metadata (optional)", "")
        require_signed_urls = st.checkbox("Require Signed URLs")

        if st.button("Upload Image"):
            response = upload_image(uploaded_image, metadata, require_signed_urls)
            response_data = response.json()

            if response_data.get("success", False):
                st.success("Image uploaded successfully!")
                st.experimental_rerun()
            else:
                st.write(response.json())
                st.error("Failed to upload image. Please check the Cloudflare API response.")

    st.header("Cloudflare Images Gallery")
    # Pagination
    pag_col1, pag_col2 = st.columns(2)
    with pag_col1:
        page_number = st.number_input("Page number", value=1, min_value=1, step=1)
    with pag_col2:
        per_page = st.number_input("Images per page", value=12, min_value=10, max_value=10000, step=10)

    # Fetch images using Cloudflare API
    response = fetch_images(page_number, per_page)
    images = response.get("result", {}).get("images", [])

    if not images:
        st.write("No images found.")
    else:
        st.write("Displaying {} images:".format(len(images)))

        # Create a grid layout with st.columns and display images with st.image()
        num_cols = 4
        col_index = 0
        for image in images:
            if col_index % num_cols == 0:
                cols = st.columns(num_cols)
            col = cols[col_index % num_cols]

            image_url_cf = "https://imagedelivery.net/-SEsWSAsICljQF4lX8NqTA/"
            image_url = f"{image_url_cf}{image.get('id')}/original"

            if image_url is not None:
                col.image(image_url, caption=image.get('filename', 'N/A'), use_column_width=True)
            else:
                # Display the error message using st.error() and remove the third argument
                col.error(f"Image details not found for {image.get('id', 'N/A')}")

            col_index += 1


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

# Upload image using Cloudflare API
def upload_image(image, metadata, require_signed_urls):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    data = {
        "metadata": json.dumps(metadata),
        "requireSignedURLs": require_signed_urls,
        "id": image.name

    }

    response = requests.post(API_BASE_URL, headers=headers, data=data, files={"file": (image.name, image)})
    return response

if __name__ == "__main__":
    main()
