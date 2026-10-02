#Finance AI Agent

import streamlit as st
from dotenv import load_dotenv

#Importing Agent
from agent import create_finance_llama_ai_agent

#Load environment variables
load_dotenv()


#Page Configuration

st.set_page_config(
    page_title="Finance AI Assistant",
    page_icon="🤖",
    layout="wide"
)

#Custom CSS

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #00FFFF;
    }

    /* Assistant message */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="stChatMessageAvatarAssistant"]
    ) {
        background-color: #00FFFF;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Assistant text */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="stChatMessageAvatarAssistant"]
    ) div[data-testid="stMarkdownContainer"] {
        color: #6B3E26 !important;
    }

    /* User message */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="stChatMessageAvatarUser"]
    ) {
        background-color: #FFF3B0;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* User text */
    div[data-testid="stChatMessage"]:has(
        div[data-testid="stChatMessageAvatarUser"]
    ) div[data-testid="stMarkdownContainer"] {
        color: #003366 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #7CFC00;
    }

    /* Spinner */
    .stSpinner > div {
        color: #003366 !important;
    }

    .stSpinner svg {
        stroke: #003366 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


#Title

st.markdown(
    """
    <h1 style="color: #6B3E26;">
        🤖 Finance AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="color: #003366;">
        Ask me about financial calculations such as EMI,
        investment calculations, percentages, and budgeting.
    </p>
    """,
    unsafe_allow_html=True
)


#Agent Initialization

agent = create_finance_llama_ai_agent()

#Sidebar Content

with st.sidebar:

    st.markdown(
        """
        <h3 style="color: #C99700;">📌 Sample Questions</h3>

        <p style="color: #C99700;">
            1. Calculate EMI for ₹10 lakh loan at 8% interest
            for 20 years.
        </p>

        <p style="color: #C99700;">
            2. If I invest ₹7000 monthly for 15 years at 10%
            return, how much will I have at the end?
        </p>

        <p style="color: #C99700;">
            3. Create a budget plan for income ₹90,000.
        </p>

        <p style="color: #C99700;">
            4. What is 20% of ₹85,000?
        </p>

        <p style="color: #C99700;">
            5. How much will I get if I invest ₹3000 per month
            for 5 years at 8% return?
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h3 style="color: #003366;">
            ℹ️ Assistant Limitations
        </h3>

        <p style="color: #003366;">
            This assistant is restricted to mathematical and
            financial calculations based on information provided
            by the user.
        </p>

        <p style="color: #003366;">
            It does not provide:
        </p>

        <p style="color: #003366;">
            • Financial advice<br>
            • Investment recommendations<br>
            • Real-time financial data
        </p>
        """,
        unsafe_allow_html=True
    )


#Session State Initialization

if "messages" not in st.session_state:
    st.session_state.messages = []

if "greeting_shown" not in st.session_state:
    st.session_state.greeting_shown = False

if "session_active" not in st.session_state:
    st.session_state.session_active = True


#Initial Greeting

if not st.session_state.greeting_shown:

    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Hello! 👋 Welcome to the Finance AI Assistant.\n\n"
            "I can help you with financial calculations such as "
            "EMI, percentages, investment calculations, and budgets.\n\n"
            "Please restrict your questions to mathematical "
            "calculations only.\n\n"
            "This assistant does not provide financial advice, "
            "investment recommendations, or real-time financial data.\n\n"
            "Please enter your calculation below."
        )
    })

    st.session_state.greeting_shown = True


#Display Chat History

for message in st.session_state.messages:

    role = message["role"]
    content = message["content"]

    if role == "user":

        with st.chat_message("user"):

            st.markdown(
                f'<div style="color:#003366;">{content}</div>',
                unsafe_allow_html=True
            )

    elif role == "assistant":

        with st.chat_message("assistant"):

            st.markdown(
                f'<div style="color:#6B3E26;">{content}</div>',
                unsafe_allow_html=True
            )


#Chat Input

user_input = st.chat_input(
    "Ask a financial calculation... "
    "Type 'clear' to clear chat or 'exit' to exit.",
    disabled=not st.session_state.session_active
)


#Process Chat Input

if user_input and st.session_state.session_active:

    command = user_input.strip().lower()

    #Clear Chat

    if command == "clear":

        st.session_state.messages = []
        st.session_state.greeting_shown = False
        st.session_state.session_active = True

        st.rerun()


    #Exit Chat

    elif command == "exit":

        # Store user's exit message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Store goodbye message
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Goodbye! 👋\n\n"
                "Thank you for using the Finance AI Assistant.\n\n"
                "This session is now inactive.\n\n"
                "Please close browser or refresh the page to start a new session.\n\n"
                "Have a great day!"
            )
        })

        # Make the session inactive
        st.session_state.session_active = False
        st.rerun()

    #Normal User Query

    else:

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        #Executing Agent with Spinner
        
        with st.spinner("Assistant is calculating..."):

            response = agent.invoke({
                "messages": st.session_state.messages
            })

        #Fetch assistant message response
        
        assistant_message = response["messages"][-1]

        answer = assistant_message.content


        
        #Extracting text from response

        if isinstance(answer, list):

            text_parts = []

            for block in answer:

                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    text_parts.append(
                        block.get("text", "")
                    )

            answer = "".join(text_parts)
        
        #Save Assistant Response
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
        
        #Refresh to display refreshed chat history
        
        st.rerun()
