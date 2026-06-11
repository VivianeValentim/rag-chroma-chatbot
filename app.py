import streamlit as st
from utils import chatbot, text
from streamlit_chat import message

def main():
    st.set_page_config(page_title="Chatbot Museum", page_icon=":books:")
    st.header("Chat with your files")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

        vectorstore = chatbot.load_existing_vectorstore()
        if vectorstore is not None:
            st.session_state.conversation = chatbot.create_conversation(vectorstore)
            st.success("Collection loaded successfully! You can start asking questions about your files.")

    user_question = st.text_input("What would you like to consult today?")

    if user_question and st.session_state.conversation:
        response = st.session_state.conversation.run(user_question)(user_question)["chat_history"]
        for i, text_message in enumerate(response):
            if i % 2 == 0:
                message(text_message.content, is_user=True, key=str(i) + "_user")
            else:
                message(text_message.content, is_user=False, key=str(i) + "_bot")

    with st.sidebar:
        st.subheader("Your Files")
        pdf_docs = st.file_uploader("Upload your PDF files here", accept_multiple_files=True)

        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing and saving to database..."):
                    all_files_text = text.process_files(pdf_docs)
                    chunks = text.create_text_chunks(all_files_text)

                    vectorstore = chatbot.create_vectorstore(chunks)
                    st.session_state.conversation = chatbot.create_conversation(vectorstore)

                    st.success("Files processed and saved successfully!")
            else:
                st.warning("Please upload at least one PDF file to process.")

if __name__ == "__main__":
    main()