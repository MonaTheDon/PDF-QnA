import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_chunks(raw_text):
    text_splittor=CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks=text_splittor.split_text(raw_text)
    return chunks

def get_vector_store(chunks):
    embeddings=abcd
    vectorstore=FAISS.from_texts(texts=chunks,embedding=embeddings)
    return vectorstore


def main():
    load_dotenv()
    st.set_page_config(page_title="QnA Model with Multiple PDFs", page_icon=":books:")

    st.header("QnA Model with Multiple PDFs :books:")
    st.text_input("Ask a Question about your documents:")

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs=st.file_uploader("Upload Your PDFs here")
        if st.button("Upload"):
            with st.spinner("Processing"):
                #get pdf text
                raw_text=get_pdf_text(pdf_docs)
                #get text chunks
                text_chunks=get_chunks(raw_text)
                #create vector store
                vector_store=get_vector_store(text_chunks)


if __name__=='__main__':
    main()