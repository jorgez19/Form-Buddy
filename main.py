import streamlit as st
import google.generativeai as genai
import io
import base64
import time

genai.configure(api_key="AIzaSyDN_52urInMoFmJzRXB-0wesim80NO3vJg")
print("started")


# Set up the model
def read_pdf_():
    with st.spinner("Analyzing..."):
        time.sleep(5)
    return "* **Pt1Line12_InCareofName[0]:** This field is typically for when you are receiving mail at an address where you don't reside (e.g., a friend's house). If this applies, ensure the name provided matches the person/entity at the address. Otherwise, leave it blank."
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

    convo = model.start_chat(history=[])
    print("1dd")
    convo.send_message(
        'Here is my input for the first 2 pages of form I-485. Tell me if i did it correctly and give me suggestions on anything that may be wrong or if I missed any required fields. Fields such as Pt1Line6_Gender[0]/Pt1Line6_Gender[1] are checkboxes so only one should be selected. This also pertains to fields ending in YN as those are \\"Yes\\" or \\"No\\" checkboxes. Also give suggestions to any fields that may be misspelled. Dates should be formatted mm/dd/yyyy. Do not give feedback on correctly answered fields : \nPt1Line1a_FamilyName[0]\nDoe\nPt1Line1b_GivenName[0]\nJohn\nPt1Line1c_MiddleName[0]\nEmpty\nPt1Line10_AlienNumber[0]\n12121\nPt1Line2a_FamilyName[0]\nEmpty\nPt1Line2b_GivenName[0]\nEmpty\nPt1Line2c_MiddleName[0]\nEmpty\nPt1Line3a_FamilyName[0]\nEmpty\nPt1Line3b_GivenName[0]\nEmpty\nPt1Line3c_MiddleName[0]\nEmpty\nPt1Line5_DateofBirth[0]\n26101985\nPt1Line6_Gender[0]\nEmpty\nPt1Line6_Gender[1]\nM\nPt1Line4a_FamilyName[0]\nEmpty\nPt1Line4b_GivenName[0]\nEmpty\nPt1Line4c_MiddleName[0]\nEmpty\nPt1Line6_CityOrTown[0]\nBueons Aires\nPt1Line10_AlienNumber[1]\nEmpty\nPt1Line8_CountryofBirth[0]\nArgentina\nPt1Line9_CountryofCitizenship[0]\nArgentina\nPt1Line12_StreetNumberName[0]\n555 Electric Ave.\nPt1Line12_Unit[0]\nEmpty\nPt1Line12_Unit[1]\nEmpty\nPt1Line12_AptSteFlrNumber[0]\nEmpty\nPt1Line12_Unit[2]\nEmpty\nPt1Line12_CityOrTown[0]\nSeattle\nPt1Line12_ZipCode[0]\n98039\nPt1Line12_State[0]\nWA\nPt1Line12_InCareofName[0]\n555879645\nPt1Line11_USCISELISAcctNumber[0]\nEmpty\nPt1Line13_StreetNumberName[0]\nEmpty\nPt1Line13_Unit[0]\nEmpty\nPt1Line13_Unit[1]\nEmpty\nPt1Line13_AptSteFlrNumber[0]\nEmpty\nPt1Line13_Unit[2]\nEmpty\nPt1Line13_CityOrTown[0]\nEmpty\nPt1Line13_ZipCode[0]\nEmpty\nPt1Line13_State[0]\nEmpty\nPt1Line13_InCareofName[0]\nEmpty\nPt1Line10_AlienNumber[2]\nEmpty\nPt1Line14_YN[0]\nN\nPt1Line14_YN[1]\nEmpty\nPt1Line15_SSN[0]\nEmpty\nPt1Line16_YN[0]\nN\nPt1Line16_YN[1]\nEmpty\nPt1Line17_YN[0]\nEmpty\nPt1Line17_YN[1]\nY\nPt1Line18_PassportNum[0]\nEmpty\nPt2Line19_TravelDoc[0]\nEmpty\nPt1Line20_ExpDate[0]\nEmpty\nPt1Line21_Passport[0]\nEmpty\nPt1Line22_VisaNum[0]\nEmpty\nPt1Line23a_CityTown[0]\nEmpty\nPt1Line23b_State[0]\nEmpty\nPt1Line24_Date[0]\nEmpty\n\n'
    )
    print("sent!")
    print(convo.last.text)
    return convo.last.text
    st.markdown(convo.last.text)


# ----------------


def get_base64_of_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


st.title("Doc Buddy")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
data = None
preview = None
if st.button("Use Test PDF"):
    # with open("test4.pdf", "rb") as f:
    #    bytes_data = f.read()
    # uploaded_test_file = io.BytesIO(bytes_data)
    print("processing...")
    result = read_pdf_()
    data = st.markdown(result)

if uploaded_file is not None:
    file_details = {
        # "FileName": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": uploaded_file.size,
    }
    st.write(file_details)

    if st.button("Process PDF"):
        file = io.BytesIO(uploaded_file.getbuffer())
        result = read_pdf_(file)
        data = st.markdown(result)


st.title("Test PDF Preview")
st.subheader("(Click Menu Icon in top-left of PDF viewer to view Full-Size)")
b64_pdf = get_base64_of_pdf("test4.pdf")
pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
