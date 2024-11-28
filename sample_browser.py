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
    ComplexCodeEval = "ComplexCodeEval"
    RepoBench = "RepoBench"
    CodeQA = "CodeQA"
    BigCodeBench = "BigCodeBench"
    WinoLogic = "Winologic"
    CruxEval = "CruxEval"

section = st.radio("Select dataset", [member.value for member in Section])

def render_repobench():
    st.subheader("RepoBench")
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


def render_codeqa():
    st.subheader("CodeQA")
    local_file_path = "codeqa_samples.jsonl"
    if os.path.isfile(local_file_path):
        file = open(local_file_path, 'rb')
    else:
        st.error('Local file not found.')
    if file.name.endswith(".jsonl"):
        samples = load_jsonl(file)
    else:
        raise Exception("Unsupported file type")
    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples[sample_idx]
    st.subheader("Code")
    st.code(sample.get("code", ""), language="python")  # Python syntax highlighting

    st.subheader("Prettified code")
    st.markdown(f"_{"I used GPT-4 to format the poorly formatted code above in the dataset ^"}_")
    st.code(sample.get("formatted_code", ""), language="python")  # Python syntax highlighting

    st.subheader("Question")
    st.write(sample.get("question", ""))
    
    st.subheader("Answer")
    st.write(sample.get("golden_answer", ""))

def render_codeqa():
    st.subheader("CodeQA")
    local_file_path = "codeqa_samples.jsonl"
    if os.path.isfile(local_file_path):
        file = open(local_file_path, 'rb')
    else:
        st.error('Local file not found.')
    if file.name.endswith(".jsonl"):
        samples = load_jsonl(file)
    else:
        raise Exception("Unsupported file type")
    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples[sample_idx]
    st.subheader("Code")
    st.code(sample.get("code", ""), language="python")  # Python syntax highlighting

    st.subheader("Prettified code")
    st.markdown(f"_{"I used GPT-4 to format the poorly formatted code above in the dataset ^"}_")
    st.code(sample.get("formatted_code", ""), language="python")  # Python syntax highlighting

    st.subheader("Question")
    st.write(sample.get("question", ""))
    
    st.subheader("Answer")
    st.write(sample.get("golden_answer", ""))

def render_bigcode_bench():
    st.subheader("BigCodeBench")
    uploaded_file = "bigcodebench-v0.1.2-00000-of-00001.parquet"
    samples = pd.read_parquet(uploaded_file)

    st.subheader("Samples for - " + uploaded_file)
    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples.iloc[sample_idx]

    for col_name, col_value in sample.items():
        st.header(col_name)
        st.code(col_value)

def render_cruxeval():
    st.subheader("CruxEval")
    jsonl_file = "cruxeval.jsonl"
    samples = pd.read_json(jsonl_file, lines=True)

    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples.iloc[sample_idx]
    for col_name, col_value in sample.items():
        st.header(col_name)
        st.code(col_value)

def render_winologic():
    st.subheader("Winologic")
    jsonl_file = "winologic.jsonl"
    samples = pd.read_json(jsonl_file, lines=True)

    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples.iloc[sample_idx]
    for col_name, col_value in sample.items():
        st.header(col_name)
        st.code(col_value)


def render_complex_code_eval():
    st.subheader("ComplexCodeEval")
    local_file_path = "ComplexCodeEval-Python-Sampled.json"
    if os.path.isfile(local_file_path):
        file = open(local_file_path, 'rb')
    samples = load_jsonl(file)
    sample_idx = st.slider("Choose a sample", 0, len(samples) - 1, 0)
    sample = samples[sample_idx]

    st.subheader("Metadata")
    metadata = f"""
    Project: {sample["git_name"]} \n 
    Version: {sample["version"]} \n 
    File path: {sample["file_path"]} \n 
    File create time: {sample["file_create_time"]} \n 
    Function update time: {sample["function_update_time"]}
    """
    st.write(metadata)
    st.subheader("Prompt")
    prompt = sample["function_signature"] + "\n" + sample["prompt"]
    st.code(prompt)
    st.write("**Dependency hints**")
    st.write(sample["function_dependencies"])

    st.subheader("Golden answer")
    st.code(sample["solution"])

    st.subheader("Context (for code completion)")
    st.write("**Context before**")
    st.code(sample["left_context"])
    st.write("**Context after**")
    st.code(sample["right_context"])


    st.subheader("Tests")
    for test in sample["test_function"]:
        st.write("**Test name**")
        st.code(test["function_name"])
        st.write("**Test implementation**")
        st.code(test["code"])

    



if section == Section.RepoBench.value:
    render_repobench()
elif section == Section.CodeQA.value:
    render_codeqa()
elif section == Section.ComplexCodeEval.value:
    render_complex_code_eval()
elif section == Section.BigCodeBench.value:
    render_bigcode_bench()
elif section == Section.WinoLogic.value:
    render_winologic()
elif section == Section.CruxEval.value:
    render_cruxeval()
else:
    st.error("Invalid section selected.")
    st.stop()