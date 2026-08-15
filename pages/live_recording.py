import streamlit as st
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time
import os

st.title("🎙️ Live Recording Assistant")
st.write("Record your meeting discussion directly using your browser microphone.")

if "live_transcript" not in st.session_state:
    st.session_state.live_transcript = ""
if "live_summary" not in st.session_state:
    st.session_state.live_summary = ""

def extract_action_items(text):
    sentences = text.split('.')
    action_keywords = ["todo", "action", "need to", "will", "assign", "complete", "by tomorrow", "next week", "deadline", "ensure"]
    found_actions = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in action_keywords):
            cleaned = sentence.strip()
            if len(cleaned) > 5:
                found_actions.append(cleaned)
    return found_actions

live_audio = st.audio_input("Record audio stream", key="live_recorder")

if live_audio is not None:
    st.audio(live_audio)
    if st.button("⚙️ Process Live Recording", type="primary"):
        unique_filename = f"live_audio_{int(time.time())}.wav"
        with open(unique_filename, "wb") as f:
            f.write(live_audio.getbuffer())
            
        with st.status("🛠️ Running Audio Pipeline...", expanded=True) as status:
            try:
                st.write("Converting speech to text...")
                recognizer = sr.Recognizer()
                with sr.AudioFile(unique_filename) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    st.session_state.live_transcript = text
                
                st.write("Summarizing with BART...")
                model_id = "sshleifer/distilbart-cnn-12-6"
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
                
                inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
                summary_ids = model.generate(**inputs, max_length=130, min_length=15, do_sample=False)
                st.session_state.live_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                
                status.update(label="✅ Complete!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(unique_filename):
                    os.remove(unique_filename)

if st.session_state.live_transcript:
    st.divider()
    st.subheader("📝 Transcript")
    st.text_area("Transcript", st.session_state.live_transcript, height=150, disabled=True)
    st.subheader("📊 Summary")
    st.text_area("Summary", st.session_state.live_summary, height=150, disabled=True)