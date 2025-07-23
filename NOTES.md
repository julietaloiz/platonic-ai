# Platonic Project Notes

## Overview
Platonic helps you think deeper by asking smart questions. It doesn’t give answers — it guides you to explore and understand ideas on your own, across all kinds of topics. 

It uses Socratic questioning to guide users, encouraging deeper reflection and understanding rather than providing direct answers.

## Purpose
- Allow users to input a topic or question.
- Respond only with follow-up questions that deepen the user's thinking.
- Help users reflect on their own ideas and assumptions.

## User Experience
- No logins required; session-based interaction only.
- Optionally ask the user for their name to personalise the session.
- No specific tone enforced for Socratic questions; can be refined in future enhancements.

## Core Features (Initial Release)
- Web-based interface for user interaction.
- AI agent that engages using Socratic questioning only (no direct answers).
- Maintains a conversation history.
- Summarises what has been explored in the conversation.

## Planned Features (Future Releases)
- Optional voice support (speech-to-text and text-to-speech).
- Random topic generation ("Surprise Me" feature).
- Downloadable session summaries (PDF/txt).

## Design Philosophy
- Focus on user-driven exploration and critical thinking.
- Minimal, clear, and distraction-free interface.
- All responses are questions to promote deeper thought.

## Tools Summary

| Function           | Tool                                  | Offline Support | Notes                                      |
| ------------------ | ------------------------------------- | --------------- | ------------------------------------------ |
| LLM agent          | LangChain + OpenAI           | Optional        | LangChain manages memory and prompt chains |
| UI                 | Streamlit                 | Yes             | Simple web app                             |
| ASR (voice input)  | `faster-whisper`                      | Yes             | Accurate and CPU-friendly                  |
| TTS (voice output) | `Coqui TTS`                           | Yes             | High-quality speech synthesis              |
| Audio I/O          | `simpleaudio` / `pyaudio`             | Yes             | For mic and playback                       |
| Summary export     | `fpdf` or `streamlit.download_button` | Yes             | Generates downloadable file                |

## Deployment

- The initial deployment will be on **Streamlit Community Cloud** for easy access and sharing.

## Core Functionalities

1. **User Inputs a Question or Topic**
   - Input field (text box) for user to type a topic or question.
   - "Surprise Me" button generates a random starter topic from a predefined list.
   - **Test:**
     - User input is stored and sent to the AI agent upon submission.
     - "Surprise Me" fills the input with a random topic and sends it to the agent.

2. **AI Responds with a Socratic Question**
   - Agent only responds with open-ended, follow-up questions (never answers).
   - Each question is relevant to the user's last message and builds on conversation history.
   - Agent remembers previous turns (uses memory).
   - **Tools:**
     - LangChain
     - Memory: ConversationBufferMemory
     - LLM: OpenAI or free alternative (e.g., GPT4All)
   - **Test:**
     - Agent responds only with a question.
     - Each question is contextually relevant (uses past messages).
     - No answers, opinions, or declarative statements in responses.

3. **Conversation Display**
   - Chat-style format showing messages from user and AI.
   - Interface clearly indicates who said what.
   - Each turn is added to the conversation log.
   - **Tools:**
     - Streamlit or Gradio
   - **Test:**
     - Messages display immediately after sending.
     - New messages appear without overwriting past ones.

4. **Running Summary of Reasoning**
   - Sidebar or separate text box updates with a summary of key ideas from the conversation.
   - Summary generated every 2–3 turns using an LLM summarisation chain.
   - **Test:**
     - Summary updates after every few turns.
     - Reflects main themes or shifts in thinking discussed so far.

5. **Voice Input (ASR)**
   - User can click a “Speak” button to provide spoken input instead of typing.
   - Speech is transcribed to text and treated like a text input.
   - **Tools:**
     - faster-whisper or whisper for speech-to-text
     - sounddevice or pyaudio for audio input
   - **Test:**
     - Speech is transcribed accurately after user finishes speaking.
     - Transcription is displayed before AI responds.
     - Transcribed text is passed to the same pipeline as typed text.

6. **Voice Output (TTS)**
   - AI's response is converted to speech and played automatically or on button click.
   - **Tools:**
     - Coqui TTS (preferred for offline use)
     - simpleaudio, playsound, or pygame for playback
   - **Test:**
     - AI response is synthesised within 1–3 seconds.
     - Audio playback matches the on-screen response.
     - No overlap between audio files (responses do not play over each other).

7. **Downloadable Session Summary**
   - After the conversation ends or after a set number of turns (e.g. 6+), user can click “Download Summary”.
   - Generates a .txt or .pdf file summarising the discussion and reasoning path.
   - **Tools:**
     - fpdf, pdfkit, or streamlit.download_button
   - **Test:**
     - Clicking “Download Summary” downloads a file with readable content.
     - File includes the full conversation log + LLM-generated summary.

8. **Starter Topic Generator**
   - Predefined list of philosophical or abstract questions is stored.
   - Clicking “Surprise Me” randomly selects one.
   - **Tools:**
     - Basic list stored in code or as CSV/json
     - Optional: shuffle or group by difficulty/themes
   - **Test:**
     - Clicking the button generates a different prompt each time.
     - Topic appears in the input field or starts the chat directly.

---

## Future Stretch Features

- **Perspective Switcher:** Ask the user to argue the opposite of their current stance.
- **Contradiction Detector:** Alert when user contradicts their earlier response.
- **Philosophical Modes:** Choose style (e.g. Empiricist, Stoic, Feminist, AI Ethicist).
- **Visual Reasoning Map:** Show branching thoughts as a concept map.
- **Multiplayer Chat:** Two users respond and AI facilitates the debate.
- **Insight Tracker:** Track what ideas the user changes over time.
- **Session Replays:** Save and reload previous dialogues.

---

## Release 1 Tasks

| # | Task | Est. Time | Notes | Done |
|---| --- | --- | --- | --- |
| 1 | Setup Project Environment in Cursor + GitHub Repo | 30 min | Create repo, virtualenv, requirements, gitignore, basic folder structure | x |
| 2 | Create rough draft file | 2 hrs | Create a py file or jupyter notebook POC with bare minimum funcitonality (e.g. prompt, question, answer, question, turn taking). It should connect tot he right apis and be interative in the console. This can be then used to split functionalities into the right scripts. | x |
| 3 | Implement Basic LangChain Socratic Agent | 1 hr | LangChain chain with conversational memory, prompt engineering, question-only responses | x |
| 4 | Build Text-Based UI (Streamlit) | 2 hrs | Chat interface, message display, input box, “Surprise Me” button placeholder |  |
| 5 | Starter Questions List + Integration | 30 min | Prepare ~20 philosophical questions, add random topic picker functionality |  |
| 6 | Running Summary Box Using LLM Summarisation | 1 hr | Summarise conversation every 2–3 turns, display on sidebar or below chat |  |
| 7 | Design and Implement Branding | 3 hrs | Choose colour palette, select fonts, design simple logo using Canva/Hatchful, store assets in repo |  |
| 8 | Integrate Branding Into UI | 1 hr | Apply colours, fonts, logo; add CSS styles in Streamlit |  |
| 9 | **Testing:** Functional tests for all above features (agent responses, UI updates, summary updates, random questions, branding consistency) | 2 hrs | Write manual test checklist; verify no crashes; test edge cases |  |
| 10 | Write README.md with Project Description, Setup, and Usage | 1 hr | Clear, concise blurb + tagline; usage instructions; screenshots/video links if available |  |
| 11 | Commit and Push to GitHub | 15 min |  |  |
| 12 | Prepare a LinkedIn Post Draft Highlighting the Project | 45 min | Include project goals, tech stack, demo GIF/screenshot, and blurb/tagline |  |

---

## Release 2 Tasks

| # | Task | Est. Time | Notes |
|---| --- | --- | --- |
| 1 | Implement Voice Input Using faster-whisper | 3 hrs | Capture mic audio, transcribe, integrate with existing text input pipeline |
| 2 | Implement Voice Output Using Coqui TTS | 3 hrs | Generate speech from AI responses, add playback controls |
| 3 | Add Toggle UI for Voice vs Text Input/Output | 1 hr | Allow switching between text and voice modes |
| 4 | Implement Downloadable Conversation Summary (TXT or PDF) | 2 hrs | Use fpdf or streamlit.download_button to generate and download summary |
| 5 | Update README + Documentation to Reflect Voice Features | 30 min | Add voice instructions and troubleshooting tips |
| 6 | **Testing:** Voice input transcription accuracy, TTS playback correctness, toggle functionality, summary generation and download integrity tests | 3 hrs | Manually test audio flows, download files, check for sync and stability |
| 7 | Commit and Push Changes to GitHub | 15 min |  |
| 8 | Create Demo Video/GIF Showing Voice Interaction | 1 hr | Screen recording with narration or captions |
| 9 | Update LinkedIn Post with Voice Features and Demo | 30 min | Refresh post, highlight added interactivity |

---

*Update this file as the project evolves. Refer to it for context in future development sessions.* 

## Further Releases

| # | Task | Est. Time | Notes |
|---| --- | --- | --- |
| 1 | Add contradiction detection and perspective switching | 4–6 hrs | LLM prompt engineering and UI updates |
| 2 | Add philosophical modes (Stoic, Empiricist, etc.) | 2–3 hrs | Mode selector + mode-specific prompt tweaks |
| 3 | Implement visual reasoning map (concept map of dialogue) | 6–8 hrs | Use JS library or Python viz libs (e.g., NetworkX, Plotly) |
| 4 | Add multi-user debate mode | 8+ hrs | Requires backend (e.g., FastAPI) + UI overhaul |
| 5 | Build session replay and insight tracking | 3–5 hrs | Save/load chat history and track belief changes |
| 6 | **Testing:** Unit and integration tests for new features and UI | As needed | Manual and/or automated testing recommended | 

## Pre-Deployment & Deployment Tasks

| # | Task | Est. Time | Notes |
|---| --- | --- |
| 1 | Prepare app for deployment (clean up code, finalize requirements.txt, freeze env) | 1 hr |  |
| 2 | Test app locally thoroughly before deployment | 1–2 hrs | Confirm no errors, all features work as expected |
| 3 | Deploy to chosen hosting platform (Streamlit Cloud / Hugging Face Spaces / Render) | 30 min | Follow deployment instructions |
| 4 | **Post-deployment testing:** Smoke test all features in deployed environment | 1–2 hrs | Confirm UI works, API calls function, voice I/O runs (if applicable), summary downloads work |
| 5 | Share deployment link on GitHub README and LinkedIn post | 30 min | Update docs and posts with live URL | 

## Data Privacy & Storage
- No conversation data is saved after the session ends; all chat history is ephemeral.
- This policy will be clearly communicated to users for transparency.
- Operational or app logs (not containing user conversation content) may be kept for debugging or analytics purposes. 

## Automated Testing
- Automated tests will be included from the beginning of development.
- Tests will be simple, minimal, and easy to understand, ensuring they do not hinder progress.
- All tests will follow general CI/CD standards for reliability and maintainability.
- Each test will be clearly documented, with an explanation of its purpose and importance.
- The goal is to catch regressions early, ensure core features work as intended, and support confident, rapid iteration. 

## Learning Goals & Collaboration
- This is a solo project for now.
- The main aim is to learn about:
  - LangChain and conversational agent design
  - Retrieval-Augmented Generation (RAG)
  - API integration (e.g., OpenAI, TTS/ASR)
  - Good development and Git practices
  - UI/UX for chatbots
- Assistance will be needed for Streamlit Community Cloud setup (secrets, environment variables, deployment) and other technical areas as they arise. 