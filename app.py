import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.llms import HuggingFaceHub
from htmlTemplates import css, bot_template, user_template


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
    # embeddings=HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    embeddings=HuggingFaceEmbeddings()
    vectorstore=FAISS.from_texts(texts=chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm=HuggingFaceHub(repo_id="google/flan-t5-xxl")
    # llm=HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-1-pythia-12b")
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
            # st.write(f"👤{message.content}")
            ques=f"👤{message.content}"
            st.write(user_template.replace("{{MSG}}", ques), unsafe_allow_html=True)
        else:
            ans=f"🤖{message.content}"
            # st.write(f"🤖{ans}")
            st.write(bot_template.replace("{{MSG}}", ans), unsafe_allow_html=True)
            st.divider()
            



def main():
    load_dotenv()
    
    st.set_page_config(page_title="QnA with Your PDF", page_icon="📚",initial_sidebar_state="expanded")
    st.write(css, unsafe_allow_html=True)

    #if app runs itself then convo is initialized it will not re-initialize it, so we can use it anytime in the program (the var is persistent)
    if "conversation" not in st.session_state:
        st.session_state.conversation=None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=None
    st.title("QnA with Your PDF 💬")
    user_question=st.text_input("Ask a Question about your documents:")
    # if user_question and flag==False:
    #     st.warning("Please click on upload PDF and wait for the confirmation message")
    if user_question:
        try:
            with st.spinner('Answering'):
                handle_userinput(user_question)
        except ValueError as e:
            #for errors by having more than 1024 tokens
            if "Input validation error: `inputs` must have less than 1024 tokens" in str(e):
                    st.warning("Error: Input has too many tokens. Please provide a shorter input or Reload")
            else:
                #for other value errors
                st.error("Error: An unexpected Value error occurred.")
        except Exception as e:
            #for other errors
            st.error("Error: An unexpected error occurred. Kindly Reload")

    with st.sidebar:
        st.subheader("Your Documents")
        
        pdf_docs=st.file_uploader("Upload Your PDFs here")
        if st.button("Upload"):
            if not pdf_docs:
                st.warning("File Not Found, Upload a File")
            elif not pdf_docs.name.endswith('.pdf'):
                st.warning("Upload a PDF File.")
            else:
                with st.spinner("Processing"):
                    #get pdf text
                    raw_text=get_pdf_text(pdf_docs)
                    #get text chunks
                    text_chunks=get_chunks(raw_text)
                    #create vector store
                    vector_store=get_vector_store(text_chunks)
                    
                    #create convo chain
                    st.session_state.conversation=get_conversation_chain(vector_store)
                    
                st.success("Uploaded Successfully!")

if __name__=='__main__':
    main()