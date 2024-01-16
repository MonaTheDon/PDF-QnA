import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

def get_pdf_text(pdf_docs):
    text=""
    pdf_reader=PdfReader(pdf_docs)
    # for pdf in pdf_docs:
    #     pdf_reader=PdfReader(pdf)
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
    embeddings=HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    vectorstore=FAISS.from_texts(texts=chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm=ChatOpenAI()
    memory=ConversationBufferMemory(memory_key='chat_history',return_messages= True)
    conversation_chain=ConversationalRetrievalChain.from_llm(llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory)
    
    return conversation_chain

def handle_userinput(user_question):
    response=st.session_state.conversation({'question':user_question})
    st.session_state.chat_history=response['chat_history']
    for i,message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(use)



def main():
    load_dotenv()
    st.set_page_config(page_title="QnA Model with Multiple PDFs", page_icon=":books:")
    #if app runs itself then convo is initialized it will not re-initialize it, so we can use it anytime in the program (the var is persistent)
    if "conversation" not in st.session_state:
        st.session_state.conversation=None

    st.header("QnA Model with Multiple PDFs :books:")
    user_question=st.text_input("Ask a Question about your documents:")
    if user_question:
        handle_userinput(user_question)

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
                #create convo chain
                st.session_state.conversation=get_conversation_chain(vector_store)
    

if __name__=='__main__':
    main()