import streamlit as st
import json
from datetime import datetime, date
from engine import classify_commitments
from agent import run_agent_turn

st.set_page_config(page_title="Executive Productivity Agent", layout="wide")

def load_data():
    with open("commitments.json", "r") as f:
        return json.load(f)

def render_brief(commitments):
    st.header("Daily Brief")
    
    my_actions = [c for c in commitments if c.get("direction") == "my_action" and c.get("status") in ["due_today", "overdue", "upcoming"]]
    waiting = [c for c in commitments if c.get("direction") == "waiting_on_other"]
    overdue = [c for c in commitments if c.get("status") == "overdue"]
    unowned = [c for c in commitments if c.get("status") == "unowned"]

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("My Actions")
        if not my_actions:
            st.info("No actions due.")
        for c in my_actions:
            status_emoji = "🔴" if c.get("status") == "overdue" else "🟡" if c.get("status") == "due_today" else "🟢"
            st.markdown(f"**{status_emoji} To {c.get('counterparty', 'Unknown').title()}**: {c.get('action')}")
            st.caption(f"Deadline: {c.get('current_deadline_text')}")
            with st.expander("History & Sources"):
                for h in c.get("status_history", []):
                    st.write(f"- {h.get('stated')}: {h.get('deadline')} (Sources: {', '.join(h.get('source_ids', []))})")
                    
        st.subheader("Overdue & At Risk")
        if not overdue:
            st.info("Nothing overdue!")
        for c in overdue:
            st.error(f"**{c.get('action')}** (was due: {c.get('current_deadline_text')})")

    with col2:
        st.subheader("Waiting on Others")
        if not waiting:
            st.info("Not waiting on anyone.")
        for c in waiting:
            st.markdown(f"**⏳ From {c.get('actor', 'Unknown').title()}**: {c.get('action')}")
            st.caption(f"Deadline: {c.get('current_deadline_text')}")
            
        st.subheader("Flagged: Unclear Ownership")
        if not unowned:
            st.info("No ownership issues.")
        for c in unowned:
            st.warning(f"**⚠️ {c.get('action')}**")
            st.caption(f"Sources: {', '.join(c.get('source_ids', []))}")

def main():
    st.sidebar.title("Agent Controls")
    
    # Time Travel control
    st.sidebar.markdown("### Simulate 'Now'")
    as_of_date = st.sidebar.date_input(
        "Current Date", 
        value=date(2026, 9, 21),
        min_value=date(2026, 9, 21),
        max_value=date(2026, 9, 25)
    )
    as_of_datetime = datetime.combine(as_of_date, datetime.min.time())
    as_of_date_str = as_of_date.strftime("%A, %d %B %Y")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    try:
        raw_commitments = load_data()
        classified = classify_commitments(raw_commitments, as_of_datetime)
    except Exception as e:
        st.error(f"Error loading commitments. Has the engine run? {e}")
        return

    # Create two columns for Brief and Chat
    main_col, chat_col = st.columns([2, 1])
    
    with main_col:
        render_brief(classified)
        
    with chat_col:
        st.header("Ask Agent")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("e.g. What did I promise Raghav?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Pass the *current* conversation history minus this latest message (which was just added)
                    # wait, run_agent_turn expects history, we can pass the whole history up to the previous turn
                    history = st.session_state.messages[:-1]
                    response = run_agent_turn(prompt, history, as_of_date_str)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
