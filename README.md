# Retrievel Augmented Generation (RAG) with Jigsaw Stack

[Frank Denneman](https://www.linkedin.com/pulse/rag-architecture-deep-dive-frank-denneman-4lple/) defines RAG this way:

> "Retrieval Augmented Generation (RAG) is a technique for augmenting Large Language Model (LLM) knowledge with additional data. In a standard Gen-AI application using LLM as its sole knowledge source, the model generates responses solely based on the input from the user query and the knowledge it has been trained on. It does not actively retrieve additional information beyond what is encoded in its parameters during fine-tuning or training. In contrast, an RAG architecture integrates both retrieval-based and generative components. It includes a retriever component that obtains relevant information from a large collection of text (typically referred to as a corpus). This corpus is stored in an embedding database, most commonly referred to as a vector database. The retrieved information is then used by the generative component to produce responses. The LLM is at the heart of the generative component."

This is a proof of concept implementation of a RAG stack using Jigsaw Stack APIs. 

## Video

[Intro video](https://youtu.be/rcQSrwwHHps)

## Set up

Create a `.env` file with the following:

```txt
JIGSAW_STACK_API_KEY = <"jigsaw_stack_api_key">
SUPABASE_PASSWORD = <"complicated_password">
```

Create a Python environment and install required packages:

```zsh
% python3 -m venv venv
% source venv/bin/activate
% pip install -r requirements.txt
```

Downloading Youtube videos requires authentication. The Youtube downloader package, [yt_dlp](https://pypi.org/project/yt-dlp/), can extract cookies from your browser and use them to authenticate to Youtube. Note that you must have previously visited Youtube. Yt_dlp is installed wih packages in `requirements.txt`. Run the following to extract your browser cookies.

```zsh
% yt-dlp --cookies-from-browser chrome --cookies cookies.txt
```

Pre-requisites checklist:
- a .env file with required key and password
- a Python environment with packages installed from requirements.txt
- a cookies.txt file with cookies from your browser 

## Start the client application

The client application uses [Streamlit](https://streamlit.io/) to run in a browser windoe. To start the application:

```zsh
% streamlit run app.py
```

## Using the client application

The client applicatin has several required inputs used for performing the RAG task. Example inputs are provided below.

- Youtube video: the Youtube video URL that we want as part of the query
    "https://www.youtube.com/watch?v=pcuwZ8zk2ng"

- Supabase query: the information from the video that we want to include in the prompt
    "current revenue report, product releases, future earnings"

- Prompt instruction: this is the item of interest in the prompt
    "Nvidia earnings"

- Respond as: this tells the LLM how to respond to the prompt
    "Jensen Wang answering investor questions"

- Question: The question or request that you want answered or returned.
    "When will Nvidia release new products and what are the expected impacts on future earnings?"

## Overview of how it works

RAG works by injecting new information into a prompt and telling an LLM to use the information in its response.

Here's how the applcation works:

1. This application extracts audio from a Youtube video using the `yt_dlp` package.  Text from the audio is extracted using [Speech to Text API](https://docs.jigsawstack.com/api-reference/ai/speech-to-text).

2. The text from the audio is processed into vectors that represent parts of the text. The vectors are stored in Supabase's vector store. While many Large Language Models (LLMs) can hold large amounts of textual information in a prompt, sorting through large bodies of text can be inefficient and cause errors. By storing the text in a vector database, we can semantically query the database for just the information we need. This creates a compact and efficient prompt and decreases the likelihood of errors.

3. The Supabase vector database is queried for information relevant for the prompt. The result is used in the prompt.

4. The app [constructs](https://docs.jigsawstack.com/api-reference/prompt-engine/create) the prompt based on the input from the client and sends the prompt to the [Prompt Engine API](https://docs.jigsawstack.com/api-reference/prompt-engine/run).

5. The responses is returned to the client and displayed in the browser.

## What's next?

The structure of this applicaiton is modular¸ and the client application can changed to perform other task. For example, the [Translate API](https://docs.jigsawstack.com/api-reference/ai/translate) we can add a Python module that can translate text extracted from a Chinese website or PDF and make it queryable using the applicaiton. The simplicity and flexibility of Jigsaw Stack makes building applications easy and fast.
