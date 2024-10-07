from backend import ESG_Bot

def response_generator(bot: ESG_Bot, query: str):
    """
    Generates response based on query of user 
    """
    return bot.get_response(query)

if __name__ == "__main__":

    import streamlit as st

    st.title("ESG Bot Demo")

    if "esg_bot" not in st.session_state: 
        st.session_state.esg_bot = ESG_Bot()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    prompt = st.chat_input("Hello! Ask me anything related to ESG in Singapore")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("ESGBot"):
            response = response_generator(bot=st.session_state["esg_bot"], query=prompt)
            st.write(response)
    
        st.session_state.messages.append({"role": "ESGBot", "content": response})


