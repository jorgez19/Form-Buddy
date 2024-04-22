import streamlit as st
import google.generativeai as genai
import io
import base64
import time
from PyPDF2 import PdfReader

st.set_page_config(page_title="Applicant", page_icon="📃")
st.sidebar.header("Applicant Buddy 📃")

genai.configure(api_key="AIzaSyDN_52urInMoFmJzRXB-0wesim80NO3vJg")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
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
            'Here is my input for the first 2 pages of form I-485. Tell me if i did it correctly and give me suggestions on anything that may be wrong or if I missed any required fields. Fields such as Pt1Line6_Gender[0]/Pt1Line6_Gender[1] are checkboxes so only one should be selected. This also pertains to fields ending in YN as those are \\"Yes\\" or \\"No\\" checkboxes. Also give suggestions to any fields that may be misspelled. Dates should be formatted mm/dd/yyyy. Do not give feedback on correctly answered fields :'
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
            print(fields[field]["/V"])
            data.append(fields[field]["/V"].replace("/", "") + "\n")
        else:
            data.append("Empty\n")
    data = " ".join(data)
    return data


# ------------------------------------------
st.title("Doc Buddy (Applicant)📃")

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
    if st.button("Use Sample I-485", type="primary"):
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


show_pdf = st.checkbox("Show Test PDF")

# If the checkbox is checked, display the test PDF
if show_pdf:
    display_test_pdf()
