#user interface
#sreamlit will automatically handle rendering it correctly
import streamlit as st
#loading PDF files
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

#load the enviroment variable from our dotenv file
load_dotenv(dotenv_path="")

#cofigure the name of the tap or page
st.set_page_config(page_title = "AI Resume Critiquer", page_icon="📄", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI powered feedback tailored to your needs!")
#load the key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#inputs
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type =["pdf","txt"])
job_role = st.text_input("Enter the job role you are taregetting (optional)")

analyze = st.button("Analyze Resume")
#takes the pdf file that is passing throught extract_text_from_file
def extract_text_from_pdf(pdf_file):
    #load the pdf using the PyPDF module
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    #look the pages
    for page in pdf_reader.pages:
        #all the text from the pdf is added to the text variable
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        #converting the reading information into BytesIO
       return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    #text file to standar texting code
    return uploaded_file.read().decode("utf-8")
#if the button was pressed, do the following
if analyze and uploaded_file:
    try:
        #get the text uploaded
        file_content = extract_text_from_file(uploaded_file)
        #remove the empty characters, if the file does not have anycontent, show an error message
        if not file_content.strip():
            #show an error message an stop the program
            st.error("File does not have any content..")
            st.stop()

        #if the file has content
        #prompt that conteint the text from the pdf
        #embed variable inside of the string
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        #passed the file content
        Resume content:
        {file_content}
        Please provide your analysis in a clear, structured format with specific recommendations."""

        #creating the client to access the open AI 
        client = OpenAI(api_key=OPENAI_API_KEY)
        #generate a response from the OpenAI
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system","content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user","content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        #print out the response
        st.markdown("### Ana")
        #we are going to get one messsage
        st.markdown(response.choices[0].message.content)
        
    except Exception as e:
        st.error(f"An error ocurred: {str(e)}")


