"""Streamlit-based negotiation simulator MVP."""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.simulator import simulate_negotiation
from utils.prompt_loader import available_agents
from utils.llm_client import get_client, list_providers


def check_setup(provider: str) -> bool:
    """Check if project is properly set up."""
    required_dirs = ["agents", "prompts", "utils"]
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            st.error(f"❌ Missing directory: {dir_name}")
            return False
    
    try:
        _ = get_client(provider=provider)
    except ValueError as e:
        st.error(
            f"❌ API Configuration Error:\n{str(e)}\n\n"
            "Create a `.env` file with proper API keys."
        )
        return False
    
    return True


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Negotiation Simulator",
        page_icon="🤝",
        layout="wide"
    )
    
    st.title("🤝 Negotiation Simulator")
    st.markdown("""
    Prepare for negotiations by practicing with AI-powered opponent agents.
    Each agent has a different style: cooperative, hard-bargaining, skeptical, or analytical.
    """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    opponent_type = st.sidebar.selectbox(
        "Opponent Type",
        options=available_agents(),
        help="Choose which negotiation opponent to face"
    )

    llm_provider = st.sidebar.selectbox(
        "LLM Provider",
        options=list_providers(),
        index=0,
        help="Choose which AI model to use for opponent responses"
    )

    # Verify setup after provider is selected
    if not check_setup(provider=llm_provider):
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### How it works:
    1. Describe your negotiation scenario
    2. Provide your opening statement/offer
    3. Receive simulated opponent response
    4. Get structured feedback on your approach
    
    **Single-turn simulation** — Make one opening, receive one response.
    """)
    
    # Main form
    st.header("📝 Scenario Setup")
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "Negotiation Topic",
            placeholder="e.g., 'Freelance contract terms' or 'Business partnership'",
            help="What are you negotiating?"
        )
        
        goal = st.text_area(
            "Your Goal",
            placeholder="e.g., 'Secure $50/hour rate with health insurance'",
            height=80,
            help="What do you want to achieve?"
        )
        
        baseline = st.text_input(
            "Minimum Acceptable (Baseline)",
            placeholder="e.g., '$45/hour with partial benefits'",
            help="Below this, the deal doesn't work for you"
        )
    
    with col2:
        batna = st.text_input(
            "BATNA (Best Alternative to Negotiated Agreement)",
            placeholder="e.g., 'Stay in current freelance work at lower rate'",
            help="Your walkaway position"
        )
        
        counterparty = st.text_area(
            "Counterparty/Organization",
            placeholder="e.g., 'Mid-size tech startup, budget-conscious'",
            height=80,
            help="Who are you negotiating with?"
        )
        
        tone = st.text_input(
            "Context/Tone",
            placeholder="e.g., Friendly but professional, first contract",
            help="Any relevant context or tone setting"
        )
    
    st.header("💬 Your Opening")
    your_opening = st.text_area(
        "Your Opening Statement or Offer",
        placeholder="Make your opening proposal or statement here...",
        height=120,
        help="What will you say to start the negotiation?"
    )
    
    # Simulation button
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    with col_btn1:
        run_button = st.button(
            "🚀 Run Simulation",
            type="primary",
            use_container_width=True,
            help="Run negotiation with selected opponent"
        )
    
    # Validation
    if run_button:
        if not all([topic, goal, baseline, batna, counterparty, your_opening]):
            st.error("❌ Please fill in all fields before running simulation.")
            st.stop()
        
        with st.spinner("🔄 Simulating negotiation..."):
            try:
                result = simulate_negotiation(
                    topic=topic,
                    goal=goal,
                    baseline=baseline,
                    batna=batna,
                    counterparty=counterparty,
                    tone=tone,
                    opponent_type=opponent_type,
                    your_opening=your_opening,
                    provider=llm_provider
                )
            except Exception as e:
                st.error(f"❌ Simulation failed: {str(e)}")
                st.stop()
        
        # Display results
        st.success("✅ Simulation complete!")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Scenario", "💭 Negotiation", "📈 Feedback"])
        
        with tab1:
            st.subheader("Structured Scenario")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("**Topic**")
                st.write(result["scenario"]["topic"])
                st.markdown("**Your Goal**")
                st.write(result["scenario"]["goal"])
                st.markdown("**Baseline**")
                st.write(result["scenario"]["baseline"])
            with col_s2:
                st.markdown("**BATNA**")
                st.write(result["scenario"]["batna"])
                st.markdown("**Counterparty**")
                st.write(result["scenario"]["counterparty"])
                st.markdown("**Context**")
                st.write(result["scenario"]["tone"])
        
        with tab2:
            st.subheader(f"Negotiation with {result['negotiation']['agent_role']}")
            st.caption(f"Provider: {result.get('provider', 'default').upper()}")
            
            st.markdown("**Your Opening Statement:**")
            st.info(result["negotiation"]["your_opening"])
            
            st.markdown(f"**{result['negotiation']['agent_role']} Response:**")
            st.success(result["negotiation"]["opponent_response"])
        
        with tab3:
            st.subheader("Structured Feedback")
            st.markdown(result["reflection"]["reflection"])


if __name__ == "__main__":
    main()
