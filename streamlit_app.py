import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Ambient Clinical Scribe",
    layout="wide",
)

st.title("🏥 Ambient Clinical Scribe")

uploaded_file = st.file_uploader(
    "Upload Consultation Audio",
    type=["mp3", "wav", "m4a"],
)

if uploaded_file:

    st.success("Audio uploaded successfully.")

    if st.button("Generate Clinical Documentation"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type,
            )
        }

        with st.spinner("Uploading audio..."):

            response = requests.post(
                f"{API_URL}/audio/upload",
                files=files,
            )

        if response.status_code != 200:
            st.error("Audio upload failed.")
            st.stop()

        audio = response.json()

        audio_id = audio["audio_id"]

        st.success("Audio uploaded.")

        with st.spinner("Generating transcript..."):

            transcript = requests.post(
                f"{API_URL}/transcript/{audio_id}"
            ).json()

        st.subheader("Transcript")

        st.write(
            transcript["transcript"]
        )

        with st.spinner("Generating SOAP note..."):

            soap = requests.post(
                f"{API_URL}/soap/{audio_id}"
            ).json()

        st.subheader("SOAP Note")

        st.json(soap)

        with st.spinner("Finding ICD recommendations..."):

            icd = requests.post(
                f"{API_URL}/icd/{audio_id}"
            ).json()

        st.subheader("ICD Recommendations")

        st.json(icd)

        report_url = f"{API_URL}/report/{audio_id}"

        report = requests.get(report_url)

        st.download_button(
            "📄 Download PDF Report",
            data=report.content,
            file_name="clinical_report.pdf",
            mime="application/pdf",
        )