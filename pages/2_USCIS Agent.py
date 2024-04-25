import streamlit as st
import google.generativeai as genai
import io
import base64
import time
from PyPDF2 import PdfReader

st.set_page_config(page_title="Agent", page_icon="📃", layout="wide")
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
            'A user inputed the following data for their form I-485 and I am to check it. Give me a list of any items that are very likely to be inccorrect. If there are any required fields that should be filled out, mention those. If there are any inconsistencies, mention those. Fields such as Pt1Line6_Gender[0]/Pt1Line6_Gender[1] are checkboxes so only one should be selected. This also pertains to fields ending in YN as those are \\"Yes\\" or \\"No\\" checkboxes. If it all looks good, simply reply "Form filled out Correctly! DO NOT give suggestions as I am not the one filling this out. I am simply checking if everything required it filled out correctly." :'
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
    div.stMarkdown {text-align:center; align-items: center; justify-content: center; !important}

    /* Center align title */
    div.stHeadingContainer {text-align:center}
    </style>
""",
        unsafe_allow_html=True,
    )
    st.title("Doc Buddy (USCIS Agent)📃")
    document_source = st.radio(
        "Choose a source for the I-485 form:",
        ("Use Sample I-485", "Upload File"),
        index=0,
    )
    st.markdown(
        "The Sample I-485 uses the first 2 pages of the I-485 for brevity of the demonstration."
    )
    if document_source == "Use Sample I-485":
        if st.button("Process Sample I-485"):
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
    # pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)


with col2:
    if document_source == "Use Sample I-485":
        display_test_pdf()
        # st.image("test4-1.png", caption="Page 1 of Sample I-485")
        # st.image("test4-2.png", caption="Page 2 of Sample I-485")
