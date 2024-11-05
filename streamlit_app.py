import streamlit as st
import google.generativeai as genai
import requests  # You may need to install this if you haven't already

# Streamlit App Title and Description
st.title("Essay Generator with Google Generative AI")
st.write("Enter a topic, and this app will generate a detailed essay for you.")

# Input field for API key and topic
api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"
topic = st.text_input("Enter the topic for the essay")

# Function to fetch statistics related to the topic
def fetch_statistics(topic):
    # Placeholder URL for a statistics API (replace with a real API)
    url = f"https://api.example.com/statistics?topic={topic}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data['statistics']  # Adjust based on actual API response structure
        else:
            st.error("Failed to fetch statistics. Please try again later.")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching statistics: {str(e)}")
        return None

# Button to trigger essay generation
if st.button("Generate Essay"):
    if not api_key or not topic:
        st.error("Please make sure to enter all fields: API Key and Topic.")
    else:
        # Configure the Google Generative AI API
        genai.configure(api_key=api_key)

        try:
            # Fetch statistics related to the topic
            statistics = fetch_statistics(topic)
            statistics_text = ""
            if statistics:
                statistics_text = "Here are some statistics related to your topic:\n" + "\n".join(statistics)

            # Create the GenerativeModel instance
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content based on the user-defined topic
            response = model.generate_content(
                f"{statistics_text}\nWrite a detailed essay on the topic: {topic}. "
                f"Give it a simplistic, student-ish language. The language should not be a long-stretch, yet should be showing reasonable confidence, "
                f"conviction and knowledge of subject. Remember to go into immaculate detail since we need the essay to be as long as possible."
            )

            # Display the generated content in Streamlit
            if response.text:
                st.subheader("Generated Essay:")
                st.write(response.text)
            else:
                st.error("No content generated. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
