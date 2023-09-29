import openai
import streamlit as st


# Image above the title
st.markdown(
    '<img src="https://i.imgflip.com/7evzrg.png" width="200" height="200">',
    unsafe_allow_html=True,
)

st.title("MIND EXPLODE BOAR CHAT")

openai.api_key = st.secrets["API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

# Initialize messages with system instruction
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "you are not an assistant, you are a boar, your only responses to anything: 'GRRGRGRGRGRAUAUGDGGGRRRRR', 'ARGH', 'AG' 'HRRRRRRRRR' and 'my mind exploded'."}]


# Render only user and assistant messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
