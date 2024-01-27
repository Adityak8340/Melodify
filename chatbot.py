import streamlit as st
from gradio_client import Client
from openai import OpenAI, AuthenticationError

image = "mld.png"

# Displaying image and title with adjusted column width
col1, col2 = st.columns([1, 3])  # Adjust the width ratios as needed

with col1:
    st.image(image, width=190)  # Adjust the width as needed

with col2:
    st.title("Your Emotions")
def lyrics_generator(prompt, user_key):
    

    client = OpenAI(api_key=user_key)
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
    {"role": "system", "content": "You are a skilled lyrics writer for songs. Emphasize musical words, ensure rhyming, and create smooth word links. Your word limit for the song is 30 words."},
    {"role": "user", "content": "Generate a song lyrics in 30 words for the prompt: " + prompt}
]
    )
    return completion.choices[0].message.content

with st.sidebar:
    st.title("How to use?")
    st.markdown("Enter your prompt in the text box below and click on the button to generate the audio.")
    st.markdown("<hr>", unsafe_allow_html=True)
    user_key = st.text_input("Enter your OpenAI API key here:")
    st.title("About")
    st.markdown("Melodify is a web app that converts your text into a song of your choice. It uses GPT-3 to generate the lyrics and HuggingFace's Bark Model to generate the audio.")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.title("Contributors")
    st.markdown("Aditya Sharma")
    st.markdown("Santosh Kumar")
    st.markdown("Dibas Kumar")
    st.markdown("Aditya Tiwari")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_key:
    if prompt := st.chat_input("what would you like to hear?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        prompt = lyrics_generator(prompt, user_key)
        prompt="♪"+prompt+"♪"
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Generating your song..."):
            client = Client("https://suno-bark.hf.space/")
            result = client.predict(prompt, "Unconditional", fn_index=3)
        st.audio(result, format="audio/wav", start_time=0)
        
        greetings = "Enjoy your Melodified song!"+ "\n" +prompt
        st.text(greetings)
        message = st.chat_message("assistant")
 
