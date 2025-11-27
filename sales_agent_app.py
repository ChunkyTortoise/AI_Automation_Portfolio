
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Sales Auto-Pilot", page_icon="🤖")

st.title("🤖 B2B Sales Auto-Pilot")
st.markdown("Enter a prospect's details below to generate a hyper-personalized outreach email.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("Your key is not stored. It is used only for this session.")

col1, col2 = st.columns(2)
contact_name = col1.text_input("Contact Name", "Elon")
company_name = col2.text_input("Company", "Tesla")
recent_news = st.text_area("Recent News / Trigger", "Cybertruck deliveries delayed due to supply chain issues.")
my_service = st.text_input("My Service", "AI-Powered Supply Chain Optimization")

if st.button("Generate Draft"):
    if not api_key:
        st.error("Please enter an OpenAI API Key in the sidebar.")
    else:
        os.environ["OPENAI_API_KEY"] = api_key
        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
            template = """
            Write a short B2B cold email to {Contact} at {Company}.
            CONTEXT: My Service: "{Service}". Their News: "{News}"
            INSTRUCTIONS: Subject line < 6 words. Hook must reference {News}. Tie news to {Service}. Under 75 words.
            """
            prompt = PromptTemplate(input_variables=["Contact", "Company", "News", "Service"], template=template)
            final_prompt = prompt.format(Contact=contact_name, Company=company_name, News=recent_news, Service=my_service)
            with st.spinner("Agent is researching and writing..."):
                response = llm.invoke(final_prompt)
                st.success("Draft Generated!")
                st.text_area("Copy Your Draft:", response.content, height=200)
        except Exception as e:
            st.error(f"Error: {e}")
