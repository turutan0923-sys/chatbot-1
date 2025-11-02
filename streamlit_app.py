import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot (Gemini API)")
st.write(
    "このチャットボットは Google Gemini API を使って応答を生成します。"
    "利用には Gemini API キーが必要です。APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) から取得できます。"
)

# Ask user for their Gemini API key.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Gemini API endpoint (プロ版はv1beta, 無料枠はv1)
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("何を話しますか？"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini expects history as context, construct it:
        context = []
        for m in st.session_state.messages:
            context.append({"role": m["role"], "parts": [m["content"]]})

        # Gemini API payload
        payload = {
            "contents": context
        }

        # Make Gemini API call
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": gemini_api_key
        }

        response_text = ""
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Gemini's response is nested. Extract the generated text.
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts:
                    response_text = parts[0].get("text", "")
        except Exception as e:
            response_text = f"❌ エラーが発生しました: {e}"

        # Display and store the response
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
