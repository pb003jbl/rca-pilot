import streamlit as st
import dspy
import pandas as pd
import agents as ag
import time as t


# Streamlit App Title
st.title("RCA AI Assistant")

chatMode = None
with st.sidebar:
        option = st.selectbox(
            "Select Mode?",
            ("Chat", "Report"),index=1
        )
        chatMode=option
        st.write("Agent Mode :", option)
        
with st.sidebar:
    # File Uploader
    uploaded_file = st.file_uploader("Upload your dataset", type=["xlsx", "csv"])
    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
      
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Dataset:")
        st.dataframe(df.head())
        ag.master_dataset=df

    



#         if st.button('Generate RCA Report'):
#             result = ag.invokeEditor()
# st.markdown(f"{result.get('report')}")
            
    # for key,value in result.items():
    #     st.write(key,value)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Generate report on dataset
# st.button('Generate Report on the dataset',key='reportButton',on_click=invokeAgents('Generate report using Report Editor'))



# React to user input
if prompt := st.chat_input("Enter Incident number OR Ask any general query about any Incident number"):
    # Display user message in chat message container
   
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    if chatMode == 'Chat':
        response = ag.invokeAssistant(prompt)
        with st.chat_message("assistant"):
            st.markdown(f"{response.get('answer')}")
    elif chatMode == 'Report':
        response = ag.invokeEditor(prompt)
        with st.chat_message("assistant"):
            st.markdown(f"{response.get('report')}")

    # Display assistant response in chat message container
    
        # for key,value in response.items():
        #    st.write(key,value)
        
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})





    



