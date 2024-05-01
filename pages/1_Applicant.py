import streamlit as st
import google.generativeai as genai
import io
import base64
import re
import time
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Agent", page_icon="📃", layout="wide")
st.sidebar.header("Applicant Buddy 📃")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


# Send data to Google Gemini to read and analyze
def read_pdf_(text):
    with st.spinner("Analyzing..."):
        convo = model.start_chat(history=[])
        with open("prompts/applicant_prompt.txt", "r") as file:
            prompt = file.read()
        convo.send_message(prompt + text)
        return convo.last.text


# Format camelstring text
def format_camel_string(input_string):
    # Insert spaces before capital letters and digits, except within all-uppercase words
    formatted_string = re.sub(r"([a-z])([A-Z0-9])", r"\1 \2", input_string)
    # Insert spaces around the word "of" (case-insensitive)
    formatted_string = re.sub(r"(?i)(\bof\b)", r" \1 ", formatted_string)
    # Remove leading and trailing spaces
    formatted_string = formatted_string.strip()
    # Merge adjacent digits (numbers) into a single word
    formatted_string = re.sub(r"(\d+)\s(\d+)", r"\1\2", formatted_string)
    # Clean up special formatting: remove specific patterns
    formatted_string = formatted_string.replace("[ 0]", "").replace("[ 1]", "").replace("_", "")
    return formatted_string


# Format Text in PDF
def format_text(doc):
    reader = PdfReader(doc)
    fields = PdfReader.get_fields(reader)
    data = []
    for field in fields:
        if not field.startswith("Pt"):
            continue
        if "/FT" in (fields[field]):
            field_new = format_camel_string(field)
            data.append(field_new + "\n")
        if "/V" in (fields[field]):
            value = fields[field]["/V"]
            if value == "/M":
                value = "Male"
            if value == "/F":
                value = "Female"
            if value == "/Y":
                value = "Yes"
            if value == "/N":
                value = "No"
            data.append(value.replace("/", "") + "\n")
        else:
            if "Gender" in field or "YN" in field:
                if "0" in field:
                    data.pop()
                    continue
                if "1" in field and field.replace("1", "0") in data:
                    data.pop()
                    continue
            data.append("Empty\n")
    data = " ".join(data)
    return data


# Left column is for main app funcitons
# Right column is displaying Test PDF
col1, col2 = st.columns([5, 4])

with col1:
    st.markdown(
        """
    <style>
    /* Center align button */
    div.stButton {text-align:center}
    
    /* Center align radio selection */
    div.stRadio [role=radiogroup]{text-align:center; align-items: center; justify-content: center; !important}
    div.stRadio [data-testid=stWidgetLabel]{text-align:center; align-items: center; justify-content: center; !important}

    /* Center align title */
    div.stHeadingContainer {text-align:center}
    </style>
""",
        unsafe_allow_html=True,
    )
    st.title("Doc Buddy (Applicant)📃")
    document_source = st.radio(
        "Choose a source for the I-485 form:",
        ("Use Sample I-485", "Upload File"),
        index=0,
    )
    st.markdown(
        "<center><sub>Note: The Sample I-485 uses the first 2 pages of the I-485 for brevity of the demonstration.</sub></center><br>",
        unsafe_allow_html=True,
    )
    if document_source == "Use Sample I-485":
        if st.button("Process Sample I-485", type="primary"):
            start_time = time.time()
            file_path = "test4.pdf"  # Example file path
            data = format_text(file_path)
            result = read_pdf_(data)  # Simulated output
            processing_time = time.time() - start_time
            col3, col4 = st.columns(2)
            with col3:
                st.metric(
                    "Doc Buddy Processing Time",
                    f"{processing_time:.2f} Seconds",
                    delta="+FAST",
                    delta_color="normal",
                    help=None,
                    label_visibility="visible",
                )
            with col4:
                st.metric(
                    "Current USCIS Processing Time",
                    "29 Months",
                    delta="-SLOW",
                    delta_color="normal",
                    help=None,
                    label_visibility="visible",
                )
            st.session_state["markdown_text_sample"] = result
        if "markdown_text_sample" in st.session_state:
            st.markdown(st.session_state["markdown_text_sample"])

    elif document_source == "Upload File":
        uploaded_file = st.file_uploader("Upload Your Completed I-485", type="pdf")
        if uploaded_file:
            data = format_text(uploaded_file)
            if st.button("Process Uploaded I-485"):
                result = read_pdf_(data)  # Simulated output
                st.session_state["markdown_text"] = result


def get_base64_of_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


def display_test_pdf():
    st.markdown(
        "<h2 style='text-align: center'>Test PDF Preview</h2>", unsafe_allow_html=True
    )
    # st.subheader("(Click Menu Icon in top-left of PDF viewer to view Full-Size)")
    b64_pdf = get_base64_of_pdf("test4-1.png")
    st.markdown(
        f"<img style='max-width: 100%;max-height: 100%;' src='data:image/png;base64, {b64_pdf}'/>",
        unsafe_allow_html=True,
    )
    b64_pdf2 = get_base64_of_pdf("test4-2.png")
    st.markdown(
        f"<img style='max-width: 100%;max-height: 100%;' src='data:image/png;base64, {b64_pdf2}'/>",
        unsafe_allow_html=True,
    )


with col2:
    if document_source == "Use Sample I-485":
        display_test_pdf()
