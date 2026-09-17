# Executive Productivity Agent (Assignment 1)

**A deterministic resolution engine and conversational agent designed to manage conflicting deadlines, ambiguous ownership, and scattered commitments across multiple data sources.**

This agent is built for **Arjun Malhotra (VP Sales)**. It ingests emails, meeting transcripts, calendars, and voice notes, then deduplicates and tracks commitments to provide a reliable Daily Brief and a conversational Q&A interface.

## 🌐 Live Demo

You can interact with the deployed prototype here:
**[https://dhruvkassignment1.streamlit.app/](https://dhruvkassignment1.streamlit.app/)**

## 🎯 Core Engineering Approach

This project is built around a specific design philosophy tailored for handling ambiguous and evolving information:

1. **Deterministic Logic Over LLM Hallucination:** The agent does *not* use an LLM to guess deadlines or ownership. If a deadline slips (e.g., the Vendor List shifting from Monday to Wednesday), a rule-based engine resolves the timeline using a `status_history` trail. If ownership is unconfirmed (e.g., the Mumbai Office Lease), the agent explicitly flags it as unowned rather than guessing.
2. **No RAG / Vector DB Overhead:** Because the provided data pack is small and finite, adding a vector database would introduce unnecessary complexity. The extraction and resolution logic happens upfront, creating a highly structured `commitments.json` store that the agent queries directly.
3. **Traceability:** Every single commitment or chat answer is grounded in actual data. The agent tracks `source_ids` back to the specific email, transcript line, or voice note that generated the task.

## 🏗️ Architecture

- **Extraction Layer:** An LLM pass structures the raw data pack into candidate commitments.
- **Resolution Engine:** A deduplication pipeline that merges duplicate actions (e.g., across a voice note and an email thread) and tracks evolving deadlines.
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
