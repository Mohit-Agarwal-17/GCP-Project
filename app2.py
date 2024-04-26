import streamlit as st
import requests
from io import BytesIO
from PyPDF2 import PdfFileReader

import base64

# Streamlit app
def main():
    st.title('PDF Merger')

    # File upload widgets
    st.header('Upload PDF Files')
    uploaded_file1 = st.file_uploader('Upload First PDF File', type='pdf')
    uploaded_file2 = st.file_uploader('Upload Second PDF File', type='pdf')

    if uploaded_file1 and uploaded_file2:
        # Merge PDFs when both files are uploaded and the button is clicked
        if st.button('Merge PDFs'):
            with st.spinner('Merging PDFs...'):
                merged_pdf_bytes = merge_pdfs(uploaded_file1, uploaded_file2)
            if merged_pdf_bytes:
                st.success('PDFs merged successfully!')
                # Display the merged PDF
                st.header('Merged PDF')
                # st.write(merged_pdf_bytes)
                # Add a download button for the merged PDF
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf_bytes,
                    file_name="merged_pdf.pdf",
                    mime="application/pdf"
                )

# Function to merge PDFs using the Flask API
def merge_pdfs(file1, file2):
    url = 'https://test-jgind7gvgq-el.a.run.app/merge_pdfs'
    files = {'file1': file1, 'file2': file2}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        merged_pdf_base64 = response.json()['merged_pdf']
        merged_pdf_bytes = base64.b64decode(merged_pdf_base64)
        return merged_pdf_bytes
    else:
        st.error('Error merging PDFs. Please try again.')

if __name__ == '__main__':
    main()
