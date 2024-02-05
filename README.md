# QnA on Your PDF 💬 using Langchain and HuggingFace API
Ask Question on your uploaded PDF and get answers

## Models
## 1. Langchain
LangChain's flexible abstractions and extensive toolkit unlocks developers to build context-aware, reasoning LLM applications. It enables applications that:

- **Are context-aware**: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.
  
- **Reason**: rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)

## 2. Google Flan T5
As OpenAI API KEY was not provided, there was a struggle in finding good LLMs that could give a good result and so we reached **FLAN-TF-xxl LLM**. There are some considerations before using the program:

a. Flan-T5 is a commercially available open-source LLM. It is a variant of the T5 (Text-To-Text Transfer Transformer) model developed by Google Research.

b. It only allows 1024 tokens so the inputs need to be small otherwise will give error.

c. It will give short word answers.

Model Link: https://huggingface.co/google/flan-t5-xxl

## Process
1. First Upload your Pdf and click on upload. Wait, as embeddings are made of your document and is stored in vectore store. 
NOTE: It takes minimum 1.5-2min while starting on a new document (Depends on document's size)
   ![image](https://github.com/MonaTheDon/PDF-QnA/assets/104318895/59a3bde5-bf5b-49af-8675-9b1175cc490d)

2. Then Add a Question and wait, as it answers. It will take a little time extra to answer first question.
3. You can answer back to back as long as it doesn't exceed the limit (1024 tokens) as it remembers the context
   ![image](https://github.com/MonaTheDon/PDF-QnA/assets/104318895/5f4c07f2-dfda-4c52-9a64-4dbb3b476e03)


## Features
1. Only PDF Files can be submitted in this application.
2. Memory Buffer is here, which means teh LLM remembers the context and so vague questions can be asked as well


## How to Set the model LOCALLY
----------------------------
To install the application, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from HuggingFace and add it to the `.env` file in the project directory.
```commandline
HUGGINGFACEHUB_API_TOKEN=your_api_key
```

Note: The variable name should only be `HUGGINGFACEHUB_API_TOKEN`


4. Run the `app.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run app.py
   ```

5. The application will launch in your default web browser, displaying the user interface.

