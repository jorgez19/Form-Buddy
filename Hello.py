import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Form Buddy! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
## Solving the Immigration Process Crisis with AI

The current waiting time to process a Form I-485 is a staggering 29 months*. Families are separated, dreams are put on hold, and the system is overwhelmed. But there's hope on the horizon.

### Our Solution
Form Buddy harnesses the power of artificial intelligence to revolutionize the immigration process. By utilizing Google's Gemini API, I've created a tool that reads and analyzes I485 forms with lightning speed and unparalleled accuracy.

### How It Works
In the **Applicant** Tab, users can submit their forms with ease. Form Buddy will not only review your submission but also offer valuable suggestions and alert you to any mistakes you may have made. Say goodbye to endless waiting and hello to a streamlined process.

### Empowering USCIS Agents
But our impact doesn't stop there. In the **USCIS Agent** tab, I demonstrate how USCIS agents can utilize Form Buddy to process forms faster and more efficiently. Think of it as your trusted assistant, guiding you through each step with precision.

*Wait times were taken from https://egov.uscis.gov/processing-times/ using the Salt Lake City office.

"""
)
