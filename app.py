import streamlit as st
import os
from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
import tiktoken
from dotenv import load_dotenv

# 🔹 Load environment variables from .env
load_dotenv()



class DebuggerState(TypedDict):
    messages: Annotated[List[Union[HumanMessage, AIMessage]], "The messages in the conversation"]
    code: str
    bugs: str
    fixed_code: str
    report: str
    test_cases: str



MAX_TOKENS = 10000

def safe_truncate(text: str, max_tokens: int) -> str:
    enc = tiktoken.encoding_for_model("gpt-4")  # Approximate tokenizer for counting
    tokens = enc.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return enc.decode(tokens[:max_tokens])

# 🔹 Read API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

bug_check_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert software developer with experience in C, C++, Python, and Java. Identify bugs in the given code and explain them.
    For each bug found:
    1. Clearly describe the issue
    2. Explain why it's problematic
    3. Provide the exact location in the code
    Format your response with clear headings for each bug."""),
    ("human", "Code:\\n{code}")
])

fix_suggestion_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a skilled software engineer. Suggest fixes for the identified bugs.
    For each bug:
    1. Restate the issue briefly
    2. Provide the exact fix needed
    3. Explain why this solution works
    Organize your response to match the bug report structure."""),
    ("human", "Code:\\n{code}\\nBugs:\\n{bugs}")
])

fix_code_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a skilled software developer proficient in C, C++, Python, and Java. Generate a corrected version of the code with all suggested fixes applied.
    Include:
    1. The complete fixed code
    2. Comments explaining the changes
    3. All original functionality preserved
    Only output the complete code with no additional commentary."""),
    ("human", "Original Code:\\n{code}\\nBugs and Fixes:\\n{bugs}")
])

report_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a software analyst. Generate a concise report on the identified bugs and fixes.
    Structure your report with:
    1. Summary of issues found
    2. Detailed explanation of each fix
    3. Impact assessment
    4. Alternative solutions considered
    Keep it professional and to the point."""),
    ("human", "Bugs:\\n{bugs}\\nFixed Code:\\n{fixed_code}")
])

test_case_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a software tester. Generate relevant test cases to verify the correctness of the fixed code.
    Include:
    1. Normal case tests
    2. Edge case tests
    3. Error case tests
    4. Brief comments explaining each test
    Format as executable Python code with assertions."""),
    ("human", "Fixed Code:\\n{fixed_code}\\nOriginal Bugs:\\n{bugs}")
])

def load_code(state: DebuggerState) -> DebuggerState:
    with open("input_code.py", "r") as f:
        code = f.read()
    truncated_code = safe_truncate(code, MAX_TOKENS)
    return {**state, "code": truncated_code, "messages": state["messages"] + [HumanMessage(content=truncated_code)]}

def check_bugs(state: DebuggerState) -> DebuggerState:
    response = llm.invoke(bug_check_prompt.format_messages(code=state["code"]))
    return {**state, "bugs": response.content, "messages": state["messages"] + [AIMessage(content=response.content)]}

def suggest_fixes(state: DebuggerState) -> DebuggerState:
    response = llm.invoke(fix_suggestion_prompt.format_messages(code=state["code"], bugs=state["bugs"]))
    return {**state, "messages": state["messages"] + [AIMessage(content=response.content)]}

def fix_code(state: DebuggerState) -> DebuggerState:
    last_fix = state["messages"][-1].content
    response = llm.invoke(fix_code_prompt.format_messages(code=state["code"], bugs=last_fix))
    with open("fixed_code.py", "w") as f:
        f.write(response.content)
    return {**state, "fixed_code": response.content, "messages": state["messages"] + [AIMessage(content=response.content)]}

def generate_report(state: DebuggerState) -> DebuggerState:
    response = llm.invoke(report_prompt.format_messages(bugs=state["bugs"], fixed_code=state["fixed_code"]))
    with open("bug_report.txt", "w") as f:
        f.write(response.content)
    return {**state, "report": response.content, "messages": state["messages"] + [AIMessage(content=response.content)]}

def generate_test_cases(state: DebuggerState) -> DebuggerState:
    response = llm.invoke(test_case_prompt.format_messages(fixed_code=state["fixed_code"], bugs=state["bugs"]))
    with open("test_cases.py", "w") as f:
        f.write(response.content)
    return {**state, "test_cases": response.content, "messages": state["messages"] + [AIMessage(content=response.content)]}

workflow = StateGraph(DebuggerState)
workflow.add_node("load_code", load_code)
workflow.add_node("check_bugs", check_bugs)
workflow.add_node("suggest_fixes", suggest_fixes)
workflow.add_node("fix_code", fix_code)
workflow.add_node("generate_report", generate_report)
workflow.add_node("generate_test_cases", generate_test_cases)

workflow.set_entry_point("load_code")
workflow.add_edge("load_code", "check_bugs")
workflow.add_edge("check_bugs", "suggest_fixes")
workflow.add_edge("suggest_fixes", "fix_code")
workflow.add_edge("fix_code", "generate_report")
workflow.add_edge("generate_report", "generate_test_cases")
workflow.add_edge("generate_test_cases", END)

def debug_python_file():
    # Initial state for the workflow
    state = {
        "messages": [],
        "code": "",
        "bugs": "",
        "fixed_code": "",
        "report": "",
        "test_cases": ""
    }
    app = workflow.compile() # Compile the workflow

    # Accumulate state from the stream
    final_state = state.copy() # Start with a copy
    for step_output in app.stream(state):
        for key, value in step_output.items():
             if isinstance(value, dict):
                 final_state.update(value)
             else:
                 pass
    return final_state

def display_results(state):
    """Display results in a tabbed interface with better formatting"""
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧐 Original Code",
        "🐞 Issues Found",
        "🛠️ Fixed Code",
        "📋 Summary Report",
        "🧪 Test Cases"
    ])

    with tab1:
        st.subheader("Original Python Code")
        st.code(state["code"], language="python")

    with tab2:
        st.subheader("Identified Issues")
        st.markdown("**Major Problems Found:**")
        st.markdown(state["bugs"])

    with tab3:
        st.subheader("Corrected Solution")
        st.code(state["fixed_code"], language="python")
        st.download_button(
            "📥 Download Fixed Code",
            data=state["fixed_code"],
            file_name="fixed_code.py",
            mime="text/python"
        )

    with tab4:
        st.subheader("Detailed Analysis")
        st.markdown("**Bug Fix Summary:**")
        st.markdown(state["report"])

    with tab5:
        st.subheader("Verification Tests")
        st.markdown("**Recommended Test Cases:**")
        st.code(state["test_cases"], language="python")

# Main App UI
st.set_page_config(page_title="Python Debugger Pro", page_icon="🐍", layout="wide")
st.title("DebugGPT")
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f0f2f6;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your code file",
            type=["py", "java", "c", "cpp"],
            help="Upload your code file (Python, C, C++, Java)"
        )

    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        debug_btn = st.button(
            "🔍 Debug Code",
            type="primary",
            disabled=not uploaded_file
        )

if uploaded_file:
    with open("input_code.py", "w") as f:
        f.write(uploaded_file.read().decode())

    if debug_btn:
        with st.spinner("🧠 Analyzing your code. Please wait..."):
            state = debug_python_file()

        st.success("✅ Debugging completed successfully!")
        st.divider()
        display_results(state)

        with st.expander("💡 Debugging Tips"):
            st.markdown("""
            - **Always test** your fixed code with different inputs
            - **Review edge cases** that might not be covered in the tests
            - **Consider performance** for recursive functions with large inputs
            - **Validate user inputs** to prevent unexpected errors
            """)