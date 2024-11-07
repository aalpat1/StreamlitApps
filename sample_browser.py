import streamlit as st
import pandas as pd
import json
import jsonlines
import os
from enum import Enum

# Function to load .jsonl file
def load_jsonl(file):
    with file as f:
        data = json.load(file)
    return data

# Function to load .csv file
def load_csv(file):
    data = pd.read_csv(file)
    return data.to_dict(orient='records')

# Upload file
# st.title("Evaluation Samples Viewer")
# file = st.file_uploader("Upload a .jsonl or .csv file", type=["jsonl", "csv"])

# Load from local file

class Section(Enum):
    RepoBench = "RepoBench"
    CodeQA = "CodeQA"
section = st.radio("Select dataset", list(Section))

def render_repobench():
    local_file_path = "samples.jsonl"
    if os.path.isfile(local_file_path):
        file = open(local_file_path, 'rb')
    else:
        st.error('Local file not found.')
    if file:
        # Load data based on file type
        if file.name.endswith(".jsonl"):
            samples = load_jsonl(file)
        else:
            samples = load_csv(file)
            
        # Toggle between samples
        sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
        sample = samples[sample_idx]
        
        sample_metadata = sample.get("sample_metadata", []) # Assumes context snippets are provided as a list
        repo = sample.get("repo", "")
        st.write("Repository:", repo)

        # Display sample details with scrollable prompt section
        st.subheader("Prompt")
        st.markdown(
            """
            <style>
            div.stCodeBlock {
                max-height: 200px;
                overflow-y: auto;
                overflow-x: hidden;
            }
            .scrollable-container {
                max-height: 200px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #ddd;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.code(sample.get("prompt", ""), language="python")  # Python syntax highlighting

        # Display context snippets with a scrollable section
        st.subheader("Context Snippets")
        context_snippets = sample_metadata.get("context_snippets", [])
        golden_context_index = int(sample_metadata.get("golden_snippet_index", 0))

        context_idx = st.slider("Choose a context snippet", 0, len(context_snippets) - 1, golden_context_index)
        context_snippet = context_snippets[context_idx]
        st.code(context_snippet, language="python")  # Adjust language as needed

        st.subheader("Golden Answer")
        st.code(sample.get("golden_response", ""), language="python")  # Adjust language as needed


if section == Section.RepoBench:
    render_repobench()
elif section == Section.CodeQA:
    st.subheader("CodeQA")
else:
    st.error("Invalid section selected.")
    st.stop()