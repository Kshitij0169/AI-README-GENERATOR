import streamlit as st
import openai
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os
import time
import json

st.set_page_config(layout="wide")
# Load environment variables from .env file
load_dotenv()
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

# Function to extract codebase details from a GitHub repository
def get_repo_files_and_contents(github_url):
    github_url = github_url.rstrip('.git')
    parts = github_url.strip("/").split("/")
    if len(parts) < 2:
        return None, "Invalid GitHub URL format."

    owner = parts[-2]
    repo = parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        repo_files = response.json()

        file_contents = {}
        for file in repo_files:
            if file['type'] == 'file' and file['name'].endswith(('.py', '.js', '.md')):  # Add or modify file types as needed
                file_url = file['download_url']
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    file_contents[file['name']] = file_response.text[:1000]  # Limit content to first 1000 chars for analysis
        return repo_files, file_contents, None

    except requests.exceptions.RequestException as e:
        return None, None, str(e)

# Streamlit app title
st.title("GitHub README Generator")

# Input for GitHub URL
github_url = st.text_input("Enter the GitHub URL:")

def clean_markdown(markdown_text):
    if markdown_text.startswith("```markdown"):
        markdown_text = markdown_text[len("```markdown"):].strip()
    if markdown_text.endswith("```"):
        markdown_text = markdown_text[:-3].strip()
    return markdown_text

def generate_readme_with_gpt(repo_files, file_contents):
    file_list = "\n".join([file['name'] for file in repo_files])
    code_summary = ""
    for filename, content in file_contents.items():
        code_summary += f"\n**{filename}**:\n{content[:500]}...\n"  # Show only the first 500 chars of each file

    prompt = f"""
    Generate a professional README.md file based on the following project structure and codebase analysis:
    
    Project Structure:
    {file_list}
    
    Codebase Features:
    {code_summary}

    Include a brief overview, installation instructions, usage examples, and any additional relevant sections. Make the README.md decorative and use emojis.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates README files for GitHub repositories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            respose_dict = response.to_dict()
            if 'choices' in respose_dict and len(respose_dict['choices']) > 0:
                readme_content = respose_dict['choices'][0]['message']['content']
                readme_content = clean_markdown(readme_content)
                return readme_content
            else:
                return "Unexpected format in GPT response."
        except openai.RateLimitError:
            st.warning("Rate limit reached. Retrying in 5 seconds...")
            time.sleep(5)
        except openai.APIConnectionError as e:
            st.error("The server could not be reached.")
            break
        except openai.APIStatusError as e:
            st.error(f"API returned a non-200 status code: {e.status_code}")
            break
    return "Failed to generate README after multiple attempts."

# Button to generate README
# Button to generate README
if st.button("Generate README"):
    if github_url:
        st.write("Fetching repository details...")

        repo_files, file_contents, error = get_repo_files_and_contents(github_url)
        if error:
            st.error(f"Error: {error}")
        else:
            st.write("Processing...")

            # Generate the README content using GPT
            readme_content = generate_readme_with_gpt(repo_files, file_contents)

            if readme_content and not readme_content.startswith("Error"):
                # Create a two-column layout
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Markdown Code")
                    st.code(readme_content, language="markdown")

                with col2:
                    st.subheader("README Preview")
                    st.markdown(readme_content, unsafe_allow_html=True)

                # Option to download the generated README if valid
                st.download_button(
                    label="Download README.md",
                    data=readme_content,
                    file_name="README.md",
                    mime="text/markdown"
                )
            else:
                st.error(f"Error generating README: {readme_content}")

    else:
        st.error("Please enter a valid GitHub URL.")


