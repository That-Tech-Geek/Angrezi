import streamlit as st
import google.generativeai as genai
import requests  # Needed for HTTP requests to Google Custom Search API

# Streamlit App Title and Description
st.title("Essay Generator with Google Generative AI")
st.write("Enter a topic, and this app will generate a detailed essay for you, enhanced with relevant statistics.")

# Input field for API key, Custom Search API key, and topic
genai_api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"
google_search_api_key = "AIzaSyAf_74VcMcZu0tZ0B1VJ-T67qTb_vA28ZE"
google_cse_id = "10a125a1f8ed84071"
topic = st.text_input("Enter the topic for the essay")

# Function to fetch statistics from Google Custom Search API
def fetch_statistics_from_google(topic):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_search_api_key,
        "cx": google_cse_id,
        "q": f"{topic} statistics",
        "num": 5  # Get the top 5 results for brevity
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            statistics = []
            for item in data.get("items", []):
                statistics.append(item.get("snippet", ""))
            return statistics
        else:
            st.error("Failed to fetch statistics. Please try again later.")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching statistics: {str(e)}")
        return None

# Button to trigger essay generation
if st.button("Generate Essay"):
    if not genai_api_key or not topic:
        st.error("Please make sure to enter all fields: API Key and Topic.")
    else:
        # Configure the Google Generative AI API
        genai.configure(api_key=genai_api_key)

        try:
            # Fetch statistics from Google search
            statistics = fetch_statistics_from_google(topic)
            statistics_text = ""
            if statistics:
                statistics_text = "Here are some statistics related to your topic:\n" + "\n".join(statistics)

            # Create the GenerativeModel instance
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content based on the user-defined topic and fetched statistics
            response = model.generate_content(
                f"{statistics_text}\nWrite a detailed essay on the topic: {topic}. "
                f"Give it a simplistic, student-ish language. The language should not be a long-stretch, yet should show reasonable confidence, "
                f"conviction, and knowledge of the subject. Remember to go into immaculate detail since we need the essay to be as long as possible."
            )

            # Display the generated content in Streamlit
            if response.text:
                st.subheader("Generated Essay:")
                st.write(response.text)
            else:
                st.error("No content generated. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
