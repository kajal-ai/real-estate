import streamlit as st
import requests
import json
import re
import os

def call_azure_ml_endpoint(endpoint_url, api_key, input_data):
    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    # Convert input data to JSON
    data = json.dumps(input_data)

    # Make the POST request
    response = requests.post(endpoint_url, headers=headers, data=data)
    print(response.text)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code: {response.status_code}, message: {response.text}")

# Streamlit app
def main():
    st.set_page_config(
        page_title="Real Estate AI Chat",
        page_icon="🏠",
    )
    st.title("Real Estate AI Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Recommend me a property for 2 million AED in Dubai with highest sales price appreciation?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call Azure ML endpoint
        endpoint_url = st.secrets["AZURE_ENDPOINT_URL"]
        api_key = st.secrets["AZURE_API_KEY"]
        
        input_data = {
            "query": prompt,
            "role": "user",
            "user_id": "auth0|66707dad1246ef15664f67c4",
            "message_id": "xyz123"
        }

        try:
            result = call_azure_ml_endpoint(endpoint_url, api_key, input_data)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                # Remove document mentions from the reply
                cleaned_reply = re.sub(r'\[doc\d+\]', '', result["reply"])
                st.markdown(cleaned_reply)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": cleaned_reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

