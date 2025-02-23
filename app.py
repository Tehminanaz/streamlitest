import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import io

import time

st.set_page_config(page_title="Futuristic Image Filter App", layout="wide")
st.markdown("""
    <style>
        body { background-color: #0d1117; color: white; }
        .stButton>button { background-color: #1f6feb; color: white; border-radius: 10px; padding: 10px 20px; }
        .stButton>button:hover { background-color: #238636; }
        .stSlider>div>div { background-color: #1f6feb; }
        .stSidebar { background-color: #161b22; padding: 10px; border-radius: 10px; color: white; }
        .header { font-size: 42px; color: #58a6ff; text-align: center; padding-bottom: 20px; }
        .subheader { font-size: 24px; color: #8b949e; padding: 10px 0; text-align: center; }
        .tooltip { font-size: 14px; color: #c9d1d9; }
        .card { background-color: #21262d; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
        .stSidebar label, .stSidebar div, .stSidebar span { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class='header'>🚀 Transform Your Images Instantly</div>
    <div class='subheader'>✨ Apply stunning filters, remove backgrounds, and elevate your creativity with our cutting-edge app!</div>
""", unsafe_allow_html=True)

# Sidebar with Filter Options
st.sidebar.markdown("<div class='subheader'>🛠️ Filter Options</div>", unsafe_allow_html=True)
st.sidebar.write("Choose from various filters and effects to enhance your image.")

# Image Uploader
uploaded_image = st.file_uploader("📤 Upload an image", type=['jpg', 'png', 'jpeg'])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.write("✅ Image uploaded successfully!")

    # Filter Options
    st.sidebar.markdown("<div class='subheader'>🎨 Apply Filters</div>", unsafe_allow_html=True)
    grayscale = st.sidebar.checkbox("Grayscale 🖤", help="Converts the image to black and white.")
    invert_colors = st.sidebar.checkbox("Invert Colors 🎨", help="Reverses the image colors.")
    brightness = st.sidebar.slider("Brightness ☀️", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast 🔲", 0.5, 2.0, 1.0, 0.1)
    sharpness = st.sidebar.slider("Sharpness 🕶️", 0.5, 3.0, 1.0, 0.1)
    blur = st.sidebar.checkbox("Blur 🌫️", help="Softens the image.")
    emboss = st.sidebar.checkbox("Emboss 🪔", help="Creates a 3D-like effect.")
    contour = st.sidebar.checkbox("Contour 🖍️", help="Highlights edges.")
    vintage = st.sidebar.checkbox("Vintage 🕰️", help="Adds a retro look.")
    cool_tone = st.sidebar.checkbox("Cool Tone ❄️", help="Enhances blue shades.")
    warm_tone = st.sidebar.checkbox("Warm Tone 🌞", help="Enhances red shades.")
    pencil_sketch = st.sidebar.checkbox("Pencil Sketch ✏️", help="Converts image to a sketch.")
    hdr_effect = st.sidebar.checkbox("HDR Effect 🌟", help="Improves details.")
    cartoon = st.sidebar.checkbox("Cartoon 🤖", help="Adds a comic style.")
    watercolor = st.sidebar.checkbox("Watercolor 🎨", help="Softens the image like watercolor.")
    remove_bg = st.sidebar.checkbox("Remove Background 🚫", help="Removes the background.")

    # Text on Image
    st.sidebar.markdown("<div class='subheader'>✍️ Add Text to Image</div>", unsafe_allow_html=True)
    add_text = st.sidebar.checkbox("Add Text 📝", help="Write custom text on the image.")
    if add_text:
        user_text = st.sidebar.text_input("Enter Text", "Your Custom Text Here")
        text_color = st.sidebar.color_picker("Pick Text Color", "#FFFFFF")
        text_size = st.sidebar.slider("Text Size", 10, 100, 30)
        text_position = st.sidebar.slider("Text Position (Y-axis)", 0, image.height, image.height // 2)

    # Apply Filters
    filtered_image = image.convert("RGB")

    if grayscale:
        filtered_image = ImageOps.grayscale(filtered_image)
    if invert_colors:
        filtered_image = ImageOps.invert(filtered_image)
    if brightness != 1.0:
        filtered_image = ImageEnhance.Brightness(filtered_image).enhance(brightness)
    if contrast != 1.0:
        filtered_image = ImageEnhance.Contrast(filtered_image).enhance(contrast)
    if sharpness != 1.0:
        filtered_image = ImageEnhance.Sharpness(filtered_image).enhance(sharpness)
    if blur:
        filtered_image = filtered_image.filter(ImageFilter.BLUR)
    if emboss:
        filtered_image = filtered_image.filter(ImageFilter.EMBOSS)
    if contour:
        filtered_image = filtered_image.filter(ImageFilter.CONTOUR)
    if vintage:
        filtered_image = ImageEnhance.Color(filtered_image).enhance(0.5)
    if cool_tone:
        r, g, b = filtered_image.split()
        filtered_image = Image.merge("RGB", (r, g, b.point(lambda i: i * 1.2)))
    if warm_tone:
        r, g, b = filtered_image.split()
        filtered_image = Image.merge("RGB", (r.point(lambda i: i * 1.2), g, b))
    if pencil_sketch:
        filtered_image = filtered_image.convert("L").filter(ImageFilter.CONTOUR)
    if hdr_effect:
        filtered_image = filtered_image.filter(ImageFilter.DETAIL)
    if cartoon:
        filtered_image = filtered_image.filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.SMOOTH)
    if watercolor:
        filtered_image = filtered_image.filter(ImageFilter.SMOOTH_MORE)
    if remove_bg:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
      
    # Add Text to Image
    if add_text and user_text:
        draw = ImageDraw.Draw(filtered_image)
        font = ImageFont.truetype("arial.ttf", text_size)
        text_bbox = draw.textbbox((0, 0), user_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (filtered_image.width - text_width) // 2
        draw.text((text_x, text_position), user_text, fill=text_color, font=font)

    # Display Images Side by Side
    st.write("## 🖼️ Image Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image", use_column_width=True)

    with col2:
        st.image(filtered_image, caption="Filtered Image", use_column_width=True)

    # Reset and Download Options
    # st.sidebar.write("---")
    # if st.sidebar.button("🔄 Reset Filters"):
    #     st.experimental_rerun()

    img_byte_arr = io.BytesIO()
    filtered_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    st.download_button(
        label="📥 Download Filtered Image",
        data=img_byte_arr,
        file_name="filtered_image.png",
        mime="image/png"
    )

    # Feature Guide
    with st.expander("💡 How to Use the App"):
        st.write("""
        1. **Upload Image:** Choose a JPG, PNG, or JPEG file.
        2. **Apply Filters:** Select filters from the sidebar and adjust sliders.
        3. **Add Text:** Write custom text, adjust size, choose its color and position.
        4. **Preview in Real-Time:** See changes instantly.
        5. **Download:** Save the final image with one click.
        6. **Background Remover:** Enable 'Remove Background' for a transparent image.
        7. **Cartoon & Watercolor:** Perfect for creative projects and social media posts.
        8. **HDR & Sharpen:** Enhance photo clarity and details effortlessly.
        """)
else:
    st.write("📤 Please upload an image to get started.")
