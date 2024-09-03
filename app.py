import fetch_audio as fa
import llm_prompt as prompt
import supabase_encode as encode
import streamlit as st

# ---
# speech to text 
# ---
def video_to_text(video_url):
    fa.download_audio(video_url)
    audio_url = fa.upload_temp_files('temp.mp3')
    text_from_audio = fa.jss_stt(audio_url)
    context = text_from_audio["text"]

    return context

def load_vectors(context):
    encode.supabase_upsert(context)

# ---
# prompt 
# ---

def run_prompt(vector_query, param_value, prompt_format, input_value):
    prompt.jss_delete_prompts()

    query_result = encode.supabase_query(vector_query)
    context = ''
    for result in query_result:
        meta = result[1]
        text = meta["text"]
        context += text

    params = prompt.jss_create_params(context, param_value, prompt_format)
    prompt_id = prompt.jss_create_prompt(params)
    input = input_value
    query = prompt.set_prompt(prompt_id, input)
    completion = prompt.jss_run_prompt(query)
    return completion["result"]

# ----
# ui
# ----

with st.form("prompt_form"):
    video_url = st.text_area("Youtube video:", None)
    vector_query = st.text_area("Supabase query:", None)
    param_value = st.text_area("Prompt instructions:", None)
    prompt_format = st.text_area("Respond as:", None)
    input_value = st.text_area("What's the question:", None)
    submitted = st.form_submit_button("Send")
    if submitted:
        text = video_to_text(video_url)
        load_vectors(text)
        result = run_prompt(vector_query, param_value, prompt_format, input_value) 
        st.write(result)