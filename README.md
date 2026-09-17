# Executive Productivity Agent (Assignment 1)

**A deterministic resolution engine and conversational agent designed to manage conflicting deadlines, ambiguous ownership, and scattered commitments across multiple data sources.**

This agent is built for **Arjun Malhotra (VP Sales)**. It ingests emails, meeting transcripts, calendars, and voice notes, then deduplicates and tracks commitments to provide a reliable Daily Brief and a conversational Q&A interface.

## 🌐 Live Demo

You can interact with the deployed prototype here:
**[https://dhruvkassignment1.streamlit.app/](https://dhruvkassignment1.streamlit.app/)**

## 🛡️ Architecture Defence & Design Decisions

This project is built around a specific design philosophy tailored for handling ambiguous and evolving information. Here is the defence of my technical choices:

### 1. Native Tool-Calling Loop vs. LangGraph/LangChain
**The Decision:** I deliberately chose to build a native, framework-free tool-calling loop (using the Groq API SDK) rather than relying on heavy orchestration frameworks like LangChain or LangGraph.
**The Defence:** For an agent with a highly scoped set of tools (three in this case), LangChain adds unnecessary bloatware, abstraction layers, and latency. Writing a native `while` loop is faster, much easier to debug, and proves a fundamental understanding of how LLM function calling actually works under the hood rather than hiding behind a framework.

### 2. Deterministic Rule-Based Resolution vs. Pure LLM
**The Decision:** The agent does *not* use an LLM to guess deadlines or ownership.
**The Defence:** When dealing with executive data, the biggest risk is hallucination. If a deadline slips (e.g., the Vendor List shifting from Monday to Wednesday), a pure Python rule-based engine resolves the timeline using a `status_history` trail. If ownership is unconfirmed (e.g., the Mumbai Office Lease where Divya only speculated it was Facilities), the agent strictly flags it as unowned. It will not hallucinate an owner. 

### 3. No RAG / Vector DB Overhead
**The Decision:** I avoided using Pinecone, Chroma, or any Vector DB for this project.
**The Defence:** The provided data pack is small and finite. Adding a vector database would introduce unnecessary complexity and infrastructure risk. Instead, the extraction (via Instructor/Pydantic) and resolution logic happens upfront, creating a highly structured, queryable `commitments.json` store that the agent can read instantly.

## 🏗️ System Flow

- **Extraction Layer:** An LLM pass (Groq + Instructor) structures the raw data pack into Pydantic models.
- **Resolution Engine:** A deduplication pipeline that merges duplicate actions and tracks evolving deadlines without generating redundant tasks.
- **Classification Engine (Time Travel):** A pure Python module that evaluates the "as-of" date to dynamically tag commitments as `due_today`, `overdue`, `upcoming`, or `unowned`.
- **Presentation (UI):** A single Streamlit application providing both a Daily Brief dashboard and a Chat interface.

## 🚀 Running the Project Locally

The project is entirely contained in a Python Streamlit app. To run it locally:

1. **Activate your virtual environment (if you have one):**
   ```bash
   source .venv/bin/activate
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API Key:**
   Create a `.env` file in the root directory and add your API key (the code expects a valid provider for the LLM client in `agent.py`):
   ```
   OPENAI_API_KEY=your_key_here
   # or ANTHROPIC_API_KEY, depending on your client setup
   ```

4. **Launch the App:**
   ```bash
   streamlit run app.py
   ```

## 🧪 Testing the Agent (Edge Cases)

To fully evaluate the agent's logic, use the **Sidebar Date Picker** to change the simulated "Current Date". Then, try asking the agent these exact prompts to see how it handles the assignment's tricky edge cases:

1. **The Evolving Deadline Test:** 
   > *"What exactly is the status of the vendor list for Raghav? When is it due?"*
   *(Tests the resolution engine's ability to track a deadline that shifted from Mon -> Tue -> Wed morning).*

2. **The Ambiguity Test:**
   > *"Who is responsible for signing the Mumbai office lease renewal?"*
   *(Tests that the agent flags this as 'unowned' rather than falsely assigning it to Facilities based on a guess).*

3. **The Multi-Source Fusion Test:**
   > *"When is my call with Meridian Logistics? Please cite your sources."*
   *(Tests the agent's ability to merge the initial calendar/transcript cancellation with the email thread rescheduling).*

4. **The Time Travel Test:**
   > *"What do I need to do today, and what is overdue?"*
   *(Change the sidebar date to Thursday, Sept 24 to verify that the agent dynamically re-classifies tasks as overdue).*

## 🛠️ Tech Stack

- **Language:** Python
- **UI Framework:** Streamlit
- **LLM Integration:** OpenAI / Anthropic SDK
- **Data Store:** Static JSON (`sources.json` and `commitments.json`)
