import streamlit as st
from utils.content_generator import generate_blog_content
from utils.image_generator import generate_image
from utils.wordpress_poster import post_to_wordpress
from utils.seo_optimizer import get_trending_keywords
import time

# Streamlit App Title
st.set_page_config(page_title="AI Blog & Image Generator", page_icon="📝", layout="centered")
st.title("📝 AI Blog & Image Generator for WordPress")

# Initialize stop state
if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False

# User Inputs
title = st.text_input("📌 Enter the Blog Title")
prompt = st.text_area("💡 Enter the Prompt for Blog Content & Image", height=150)

# Fetch Trending Keywords
if st.button("🔥 Get Trending Keywords"):
    if not prompt:
        st.warning("⚠ Please enter a topic first!")
    else:
        trends = get_trending_keywords(prompt)
        if "error" in trends:
            st.error(trends["error"])
        else:
            st.subheader("📈 Trending Keywords (Google Trends - India)")
            st.write(f"🔹 **Top Keywords:** {', '.join(trends['top_keywords'])}")
            st.write(f"🚀 **Rising Keywords:** {', '.join(trends['rising_keywords'])}")

# Button to Stop Process
if st.button("🛑 Stop"):
    st.session_state.stop_generation = True  # Set stop flag
    st.warning("⚠ Process Stopped!")

# Button to Generate Blog
if st.button("🚀 Generate & Publish to WordPress"):
    if not title or not prompt:
        st.warning("⚠ Please fill in both the title and the prompt.")
    else:
        st.session_state.stop_generation = False  # Reset stop state

        try:
            with st.spinner("Generating content... 🧠"):
                for i in range(5):  # Simulating stepwise generation
                    if st.session_state.stop_generation:
                        st.warning("⚠ Process Stopped by User!")
                        st.stop()

                    time.sleep(1)  # Simulate some delay

                content = generate_blog_content(prompt)
                image_path = generate_image(prompt)
                message = post_to_wordpress(title, content, image_path)

            st.success(message)
            st.subheader("Generated Image:")
            st.image(image_path, caption="AI-Generated Image")

            st.subheader("Generated Blog Content:")
            st.write(content)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown(
   """
---
Built using cutting-edge AI technology.
"""
)
