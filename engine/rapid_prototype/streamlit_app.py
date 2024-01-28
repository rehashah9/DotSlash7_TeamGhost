import streamlit as st
import random
import time
from dotenv import load_dotenv
load_dotenv()
from st_pages import Page, Section, show_pages, add_page_title
from helper.connection import get_list_of_connections
from api.main import get_user_query_stageone
import google.generativeai as genai
from tabulate import tabulate

genai.configure(api_key="AIzaSyAZzGyJ9DlHZYjmTJHR33FkmN09LU0W8-Q")

# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

st.sidebar.title("Cloud Connection")
show_pages(
        [
            Page("streamlit_app.py", "Chat", "💬"),
            Page("pages/page_configuration.py", "Configuration", ":electric_plug:"),
            Page("pages/page_thrifty.py", "Thrifty", "💰"),
            Page("pages/page_graph.py", "Monitoring", ":bar_chart:"),
            Section("My section", icon="🎈️")
        ]
    )
st.title("Cloud GPT-3 Chatbot Prototype")
selected_option = ""


if "list_of_connection" not in st.session_state.keys(): # Initialize the chat engine
    st.session_state.list_of_connection = get_list_of_connections()


selected_option = st.sidebar.selectbox(
        'Select Connection',
        st.session_state.list_of_connection
    )
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        alpha_data = get_user_query_stageone(prompt, "aws_demo", "aws_ec2")

        print("This is Data: ",alpha_data)
        alpha_prompt = ""

        alpha_prompt += (open("./data/chat_aws_ec2.txt","r")).read()
        alpha_prompt += "Data: " + str(alpha_data)

        prompt_parts = [
            alpha_prompt,
            "User Input: " + prompt,
        ]
        
        full_response = ""

        table = tabulate(alpha_data, headers="keys", tablefmt="pipe")


        # response = model.generate_content(prompt_parts, stream=True)
        # for chunk in response:
        #     full_response += chunk.text + " "
        #     message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(table)
        # print(response)
        # Simulate stream of response with milliseconds delay
        # for chunk in assistant_response.split():
        #     full_response += chunk + " "
        #     time.sleep(0.05)
        #     # Add a blinking cursor to simulate typing
        #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})