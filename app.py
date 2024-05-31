import streamlit as st
from moviepy.editor import VideoFileClip
from mutagen.mp4 import MP4, MP4Cover
import tempfile
import os

# Inject custom CSS
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #111;
}
.css-2trqyj {
    background-color: #0068c9;
    border-color: #005cbf;
}
.stButton>button {
    color: #fff;
    background-color: #0068c9;
    border-color: #005cbf;
}
</style>
""", unsafe_allow_html=True)

st.title("Video Thumbnail Adder")

# File uploader for video
video_file = st.file_uploader("Upload your video file", type=['mp4', 'mov', 'm4v'])
image_file = None

if video_file:
    st.success("Video uploaded successfully!")
    if st.button("Add Thumbnail"):
        # Create a session state to manage the appearance of the image uploader
        st.session_state.show_image_uploader = True

# Check if the session state is set to show the image uploader
if 'show_image_uploader' in st.session_state and st.session_state.show_image_uploader:
    image_file = st.file_uploader("Now upload your image file", type=['png', 'jpg', 'jpeg'])

if video_file and image_file:
    st.success("Image uploaded successfully!")

    # Submit button for processing
    if st.button("Submit"):
        with st.spinner('Processing...'):
            # Temporarily save files
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[1]) as vf:
                vf.write(video_file.getvalue())
                video_path = vf.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as imgf:
                imgf.write(image_file.getvalue())
                img_path = imgf.name

            # Load video and image
            video = MP4(video_path)
            with open(img_path, 'rb') as img:
                video["covr"] = [
                    MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG if img_path.lower().endswith('.jpeg') or img_path.lower().endswith('.jpg') else MP4Cover.FORMAT_PNG)
                ]
            
            # Save the video with thumbnail
            video.save(video_path)
            st.success("Thumbnail added successfully!")
            
            # Download button (enabled only after processing is done)
            with open(video_path, "rb") as file:
                btn = st.download_button(
                    label="Download video with thumbnail",
                    data=file,
                    file_name=video_file.name,
                    mime="video/mp4"
                )
            # Clean up temporary files
            os.unlink(video_path)
            os.unlink(img_path)

else:
    if video_file and not image_file and 'show_image_uploader' in st.session_state and st.session_state.show_image_uploader:
        st.warning("Please upload an image file to proceed.")