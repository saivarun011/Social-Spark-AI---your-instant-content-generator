import streamlit as st
import os
import requests
import json

# --- Ollama Configuration ---
# IMPORTANT: Make sure Ollama is installed and running in a separate Command Prompt window.
# Run ollama run llama2 in that window before starting this Streamlit app.
OLLAMA_API_URL = "http://localhost:11434/api/generate" # Default Ollama API endpoint
OLLAMA_MODEL = "llama2" # This MUST match the model you downloaded and are running (e.g., "llama2", "mistral")

# --- Streamlit Web App Interface Setup ---
st.set_page_config(page_title="Social Spark AI", layout="centered")

st.title("✨ Social Spark AI")
st.markdown("Your Instant Content Generator for social media posts & headlines!")

# --- User Input Fields ---
# These define the input boxes and dropdowns on your web application
topic = st.text_area(
    "What's your post about? (e.g., 'new organic coffee launch', 'tips for remote work')",
    height=100,
    key="topic_input"
)

platform = st.selectbox(
    "Target Social Media Platform:",
    ("Instagram", "Twitter/X", "LinkedIn", "Facebook", "Blog Headline"),
    key="platform_select"
)

tone = st.selectbox(
    "Desired Tone:",
    ("Casual and Exciting", "Professional and Informative", "Humorous", "Salesy", "Thought-Provoking"),
    key="tone_select"
)

num_posts = st.slider(
    "Number of ideas to generate:", 1, 5, 3, # Slider from 1 to 5 ideas, starting at 3
    key="num_posts_slider"
)

# --- Logic for the "Generate Ideas" Button ---
if st.button("Generate Ideas", key="generate_button"):
    if not topic:
        # Display a warning if the topic field is empty
        st.warning("Please tell me what your post is about!")
    else:
        # Show a spinner while the AI is generating content
        with st.spinner("Sparking creativity..."):
            # Construct the prompt for the Ollama model based on user inputs
            prompt_template = f"""Generate {num_posts} {tone} social media post ideas for {platform} about: {topic}. Each idea should be concise and engaging. Format each idea on a new line."""

            try:
                # Prepare the data payload for the Ollama API request
                data = {
                    "model": OLLAMA_MODEL,
                    "prompt": prompt_template,
                    "stream": False # Set to False to get the full response at once
                }

                # Send the POST request to your local Ollama server
                response = requests.post(OLLAMA_API_URL, json=data)
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

                # Parse the JSON response from Ollama
                response_json = response.json()
                # Extract the generated text from the 'response' field in the JSON
                generated_text = response_json.get("response", "No response from local model.")

                st.subheader("💡 Your Ideas:")
                # Split the generated text into individual post ideas based on newlines
                posts = generated_text.strip().split('\n')
                # Display each idea in a separate text area
                for i, post in enumerate(posts):
                    if post.strip(): # Only display non-empty lines
                        st.text_area(f"Idea {i+1}", post.strip(), height=100, key=f"generated_post_{i}")

            except requests.exceptions.ConnectionError:
                # Error handling if the Streamlit app can't connect to Ollama
                st.error("Error: Could not connect to Ollama. Is Ollama running and have you downloaded a model?")
                st.info(f"Make sure Ollama is installed and run ollama run {OLLAMA_MODEL} in a separate Command Prompt window.")
            except Exception as e:
                # General error handling for any other issues during the process
                st.error(f"Oops! Something went wrong with the local model: {e}. Please try again.")
                st.info("Tip: Ensure your OLLAMA_MODEL in app.py matches the model you've downloaded and are running.")

# Optional: Add a footer to your Streamlit app
st.markdown("---")
st.caption("Powered by Ollama and Streamlit")
st.markdown("Project by [B.Saivarun/Social-Spark-AI (Your Instant Content Generator)]")