import streamlit as st
import google.generativeai as genai
import io
import base64
import time
from PyPDF2 import PdfReader

st.set_page_config(page_title="Agent", page_icon="📃")
st.sidebar.header("USCIS Agent Buddy 📃")
genai.configure(api_key="AIzaSyDN_52urInMoFmJzRXB-0wesim80NO3vJg")
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
print("loading...")
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
print("started")


# Set up the model
# @st.cache_data
def read_pdf_(text):
    with st.spinner("Analyzing..."):
        convo = model.start_chat(history=[])
        print("1dd")
        convo.send_message(
            'A user inputed the following data for their form I-485 and I am to check it. Give me a list of any items that are very likely to be inccorrect. If there are any required fields that should be filled out, mention those. If there are any inconsistencies, mention those. If it all looks good, simply reply "Form filled out Correctly!" :'
            + text
        )
        print("sent!")
        print(convo.last.text)
        return convo.last.text


# ----------------


def get_base64_of_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


# ------------------------------------------


def format_text(doc):
    reader = PdfReader(doc)
    fields = PdfReader.get_fields(reader)
    data = []
    for field in fields:
        if not field.startswith("Pt"):
            continue
        if "/FT" in (fields[field]):
            print(fields[field]["/FT"])
            data.append(field + "\n")
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
            data.append("Empty\n")
    data = " ".join(data)
    return data


# ------------------------------------------
st.title("Doc Buddy (USCIS Agent)📃")

uploaded_file = st.file_uploader(
    'Upload Your Completed I-485 (or press "Use Sample I-485" Button)', type="pdf"
)

st.markdown(
    "The Sample I-485 uses the first 2 pages of the I-485 for brevity of the demonstration."
)


if uploaded_file is not None:
    data = format_text(uploaded_file)
    # print(data)

    if st.button("Process PDF"):
        start_time = time.time()
        result = read_pdf_(data)
        processing_time = time.time() - start_time
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Doc Buddy Processing Time",
                f"{processing_time:.2f} Seconds",
                delta="+FAST",
                delta_color="normal",
                help=None,
                label_visibility="visible",
            )
        with col2:
            st.metric(
                "Current USCIS Processing Time",
                "29 Months",
                delta="-SLOW",
                delta_color="normal",
                help=None,
                label_visibility="visible",
            )
        st.session_state["markdown_text"] = result
else:
    if st.button("Use Sample I-485"):
        print("processing...")
        start_time = time.time()
        data = format_text("test4.pdf")
        result = read_pdf_(data)
        processing_time = time.time() - start_time
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Doc Buddy Processing Time",
                f"{processing_time:.2f} Seconds",
                delta="+FAST",
                delta_color="normal",
                help=None,
                label_visibility="visible",
            )
        with col2:
            st.metric(
                "Current USCIS Processing Time",
                "29 Months",
                delta="-SLOW",
                delta_color="normal",
                help=None,
                label_visibility="visible",
            )
        st.session_state["markdown_text"] = result

if "markdown_text" in st.session_state:
    st.markdown(st.session_state["markdown_text"])


def display_test_pdf():
    st.title("Test PDF Preview")
    st.subheader("(Click Menu Icon in top-left of PDF viewer to view Full-Size)")
    b64_pdf = get_base64_of_pdf("test4.pdf")
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


show_pdf = st.checkbox("Show Test PDF")

# If the checkbox is checked, display the test PDF
if show_pdf:
    display_test_pdf()
