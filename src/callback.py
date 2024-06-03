import streamlit as st
from .utils import completion, include_context_in_prompt

def clear_chat_history():
    st.session_state.messages = []

def increment_nb_prompts():
    st.session_state.nb_prompts += 1

def decrement_nb_prompts():
    st.session_state.nb_prompts -= 1

def display_intermediate_answers():
    st.session_state.display_intermediate_answers = not st.session_state.display_intermediate_answers

def use_context():
    st.session_state.use_context = not st.session_state.use_context

def generate_answer(api_key: str, model: str):
    """
    Expect to have [i] in the prompt i+1 if you want to use the output of the prompt i for the prompt i+1 
    """
    st.session_state.messages = []
    prompt = st.session_state["prompt_0"]
    st.session_state["messages"].append({"role":"user", "content":prompt})
    answer = completion(prompt, api_key, model)
    answers = [answer]
    st.session_state["messages"].append({"role":"assistant", "content":answer})
    for i in range(1, st.session_state.nb_prompts):
        prompt = st.session_state[f"prompt_{i}"].replace(f"[{i}]", answers[-1])
        prompt = include_context_in_prompt(st.session_state["messages"], prompt, model) if st.session_state.use_context else prompt
        st.session_state["messages"].append({"role":"user", "content":prompt})
        answer = completion(prompt, api_key, model)
        st.session_state["messages"].append({"role":"assistant", "content":answer})