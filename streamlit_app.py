import streamlit as st
import google.generativeai as genai

# Streamlit App Title and Description
st.title("Essay Generator with Google Generative AI")
st.write("Enter a topic, and this app will generate a detailed 5000-word essay for you.")

# Input field for API key and topic
api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"
topic = st.text_input("Enter the topic for the essay")

# Button to trigger essay generation
if st.button("Generate Essay"):
    if not api_key or not topic:
        st.error("Please make sure to enter all fields: API Key and Topic.")
    else:
        # Configure the Google Generative AI API
        genai.configure(api_key=api_key)

        try:
            # Create the GenerativeModel instance
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content based on the user-defined topic
            response = model.generate_content(f"Write a detailed essay on the topic: {topic}. Go into every single detail, write it extremely long, AND I MEAN IT.")

            # Display the generated content in Streamlit
            if response.text:
                st.subheader("Generated Essay:")
                st.write(response.text)
            else:
                st.error("No content generated. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
