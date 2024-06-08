import streamlit as st
import pandas as pd
import numpy as np

from openai import OpenAI
from src.callback import *

st.set_page_config(page_title="Prompter",page_icon="🛠️",)

############# Session States #############
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nb_prompts" not in st.session_state:
    st.session_state.nb_prompts = 1
if "display_intermediate_answers" not in st.session_state:
    st.session_state.display_intermediate_answers = False
if "use_context" not in st.session_state:
    st.session_state.use_context = False

############# Main #############
with st.expander("**:bulb: AI settings**", expanded=True):
    c1, c2 = st.columns(2)

    model = c1.selectbox("Model", options=["gpt-3.5-turbo", "gpt-3.5-turbo-instruct","gpt-4", "gpt-4-turbo"])
    api_key = c2.text_input("OpenAI API key", type="password", placeholder="This will never be stored")
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, step=0.01, value=1.0,
                            help="Controls the “creativity” or randomness of the output. Higher temperatures (e.g., 0.7) result in more diverse and creative output (and potentially less coherent), while a lower temperature (e.g., 0.2) makes the output more deterministic and focused.")
    top_p = st.slider("Top p", min_value=0.0, max_value=1.0, step=0.01, value=1.0,
                    help="Consider only the possibilities that equal or exceed the top p value. Kind of a similar effect as the temperature")
    freq_penalty = st.slider("Frequency Penalty", min_value=-2.0, max_value=2.0, step=0.01, value=0.0,
                        help="Penalize tokens that were sampled too much prior to the current position")
    presence_penalty = st.slider("Presence Penalty", min_value=-2.0, max_value=2.0, step=0.01, value=0.0,
                    help="Penalize tokens that were at least sampled once prior to the current position")

with st.expander("**:bookmark_tabs: Prompt Settings**", expanded=True):
    st.button('Add a prompt', on_click=increment_nb_prompts)
    st.button('Remove a prompt', on_click=decrement_nb_prompts)
    st.toggle('Display intermediate answers', on_change=display_intermediate_answers)
    st.toggle('Use context', on_change=use_context)

with st.expander("**:arrow_forward: Prompts**", expanded=True):
    for i in range(st.session_state.nb_prompts):
        if i == 0:
            st.text_area(f'Prompt {i+1}', key=f'prompt_{i}', placeholder="To use the output of the prompt i in the following prompts, type [i].\nFor example : 'Add the following two numbers : [1] and [2]'")
        else:
            st.text_area(f'Prompt {i+1}', key=f'prompt_{i}')
    st.button("Generate answer", use_container_width=True, on_click=generate_answer, kwargs={"api_key":api_key, "model":model})

# for i in range(st.session_state.nb_prompts):
#     st.write(st.session_state[f"prompt_{i}"])

# st.write(st.session_state.messages)
if st.session_state.messages:
    with st.expander("**:arrow_forward: Answers**", expanded=True):
        if st.session_state.display_intermediate_answers:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        else:
            last_message = st.session_state.messages[-1]
            with st.chat_message(last_message["role"]):
                st.write(last_message["content"])
        st.button("Clear Chat History", on_click=clear_chat_history)

