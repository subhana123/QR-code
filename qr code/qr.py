import streamlit as st
import qrcode
from PIL import Image
import io
import cv2
import numpy as np

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def decode_qr_code(image_file):
    image = Image.open(image_file)
    image_np = np.array(image)
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(gray_image)
    return data

def main():
    st.set_page_config(page_title="QR Code Encoder/Decoder", page_icon="📱")
    st.title("📱 QR Code Encoder/Decoder")

    st.header("Generate QR Code")
    text_input = st.text_input("Enter text to encode:")
    if st.button("Generate QR Code") and text_input:
        qr_image = generate_qr_code(text_input)
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        st.image(buffer, caption="Generated QR Code")
        st.download_button("Download QR Code", data=buffer.getvalue(), file_name="qrcode.png", mime="image/png")

    st.header("Decode QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code image to decode", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        decoded_text = decode_qr_code(uploaded_file)
        if decoded_text:
            st.success(f"Decoded text: {decoded_text}")
        else:
            st.error("No valid QR code found. Please try another image.")


if __name__ == "__main__":
    main()
