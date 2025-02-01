import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }

    /* Model-specific chat message colors */
    .deepseek-r1 {
        background-color: #4b7465;
        background-image: linear-gradient(132deg, #4b7465 0%, #096453 50%, #062b51 100%);
    }
    .deepseek-coder {
        background-color: #16a394;
        background-image: linear-gradient(315deg, #16a394 39%, #0d0b93 99%);
    }
    .medllama2 {
        background-color: #d3087c;
        background-image: linear-gradient(225deg, #d3087c 0%, #784BA0 46%, #064674 100%);    
    }
</style>
""", unsafe_allow_html=True)

st.title("Companion")
st.caption("An AI assistant to help you get better!")

model_capabilities = {
    "Choose a model": [],
    "deepseek-r1:1.5b": [
        "🔘Parameters : 1.5 billion",
        "💻 Code Expert",
        "🐞 Debugging Assistant",
        "📝 Code Documentation",
        "💡 Solution Architect",
    ],
    "deepseek-coder:1.3b": [
        "🔘Parameters : 1.3 billion",
        "📜 Code Generation",
        "🎯 Algorithm Optimization",
        "🔍 Code Review",
        "🚀 Performance Tuning",
    ],
    "medllama2:latest": [
        "🔘Parameters : 3.6 billion",
        "⚕️ Medical Knowledge",
        "🩺 Clinical Text Analysis",
        "🧬 Biomedical Research",
        "📊 Data Interpretation",
    ],
}

ability_selection = {
    0.0: {
        "description": """
        🤖 **Strict Factual Mode** (0.0)
        - 100% deterministic outputs
        - Best for code compilation/execution
        - Zero creativity, maximum reproducibility
        - Use for: Syntax fixes, API documentation
        """
    },
    0.1: {
        "description": """
        🔍 **Precision Mode** (0.1)
        - Almost deterministic
        - Minimal creativity allowed
        - Good for: Debugging, error analysis
        - Maintains strict code conventions
        """
    },
    0.2: {
        "description": """
        📚 **Technical Assistant** (0.2)
        - Balanced technical focus
        - Slight creativity in problem solving
        - Use for: Code optimization, architecture
        - Maintains strong factual accuracy
        """
    },
    0.3: {
        "description": """
        👩💻 **Developer Default** (0.3)
        - Optimal coding balance
        - Allows some solution exploration
        - Good for: General coding tasks
        - Default for technical assistance
        """
    },
    0.4: {
        "description": """
        💡 **Creative Coder** (0.4)
        - Moderate creativity
        - Explains alternative approaches
        - Use for: Algorithm design, brainstorming
        - Maintains technical coherence
        """
    },
    0.5: {
        "description": """
        🎨 **Balanced Thinker** (0.5)
        - Equal balance logic/creativity
        - Good for: Solution comparison
        - Generates multiple valid options
        - Suitable for design discussions
        """
    },
    0.6: {
        "description": """
        🌱 **Innovation Mode** (0.6)
        - Creative problem solving
        - May suggest novel approaches
        - Use for: Prototyping, POC development
        - Monitor for accuracy
        """
    },
    0.7: {
        "description": """
        🚀 **Brainstorm Mode** (0.7)
        - High creativity
        - Explores unconventional solutions
        - Good for: Feature ideation
        - Verify technical feasibility
        """
    },
    0.8: {
        "description": """
        🔮 **Visionary Mode** (0.8)
        - Very high randomness
        - Blue-sky thinking
        - Use for: Concept exploration
        - May require fact-checking
        """
    },
    0.9: {
        "description": """
        🎲 **Random Explorer** (0.9)
        - Maximum creativity
        - Unpredictable outputs
        - Good for: Inspiration generation
        - Not recommended for production code
        """
    }
}

with st.sidebar:
    st.header("⚙️ Configuration")

    # Initialize session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = list(model_capabilities.keys())[0]
    if "selected_temp" not in st.session_state:
        st.session_state.selected_temp = 0.0  # Default temp

    # Model selection
    selected_model = st.selectbox(
        "Choose Model",
        list(model_capabilities.keys()),
        index=list(model_capabilities.keys()).index(st.session_state.selected_model)
    )

    # Temperature selection
    selected_temp = st.slider(
        "Select Creativity Level",
        min_value=0.0,
        max_value=0.9,
        step=0.1,
        value=st.session_state.selected_temp  # Use session state value
    )

    # Check if model or temperature is changed
    if selected_model != st.session_state.selected_model or selected_temp != st.session_state.selected_temp:
        st.session_state.selected_model = selected_model
        st.session_state.selected_temp = selected_temp
        st.rerun()

    # Model capabilities
    st.markdown("### Model Capabilities")
    for capability in model_capabilities[selected_model]:
        st.markdown(f"- {capability}")
    
    st.divider()
    
    # Display temperature mode description
    st.markdown(ability_selection[selected_temp]["description"])

# initiate the chat engine
llm_engine = ChatOllama(
    model=st.session_state.selected_model,
    base_url="http://localhost:11434",
    temperature=float("%.2f" % st.session_state.selected_temp)
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI assistant. Provide concise, correct solutions "
    "with strategic statements for solution to problem . Always respond in English."
)

if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": f"Hi! I'm {st.session_state.selected_model}. How can I help you today?"}]
else:
    # Update the initial AI message when the model is changed
    if st.session_state.message_log[0]["role"] == "ai":
        st.session_state.message_log[0]["content"] = f"Hi! I'm {st.session_state.selected_model}"

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        # Determine the CSS class based on the model
        if message["role"] == "ai":
            if st.session_state.selected_model == "deepseek-r1:1.5b":
                css_class = "deepseek-r1"
            elif st.session_state.selected_model == "deepseek-coder:1.3b":
                css_class = "deepseek-coder"
            elif st.session_state.selected_model == "medllama2:latest":
                css_class = "medllama2"
            else:
                css_class = ""
            
            with st.chat_message(message["role"], avatar="🤖"):
                st.markdown(f'<div class="{css_class}" style="padding: 10px; border-radius: 5px;">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input(f"Type your question here....")

def generate_ai_response(prompt_chain):
    processing_pipeline=prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        # Escape curly braces in message content
        escaped_content = msg["content"].replace("{", "{{").replace("}", "}}")
        
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(escaped_content))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(escaped_content))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()