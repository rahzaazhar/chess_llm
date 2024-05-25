import io
import streamlit as st
from chessstory import ChessStoryGen, system_prompt

storygenerator = ChessStoryGen(system_prompt=system_prompt)
def process_file(file):
    # Dummy function to simulate file processing
    content = file.read().decode('utf-8')
    processed_text = f"Processed text from the uploaded file:\n\n{content}"
    return processed_text

st.title("File Upload and Processing")


uploaded_file = st.file_uploader("Upload Chess Game in PGN format", type=['pgn'])

if uploaded_file is not None:
    uploaded_file = uploaded_file.read().decode('utf-8')
    uploaded_file = io.StringIO(uploaded_file)
    processed_text = storygenerator.generate_story(pgn=uploaded_file)
    st.text_area("Processed Text", processed_text, height=300)
