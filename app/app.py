from math import trunc
import os
import ast
import io
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages.base import BaseMessage

from helpers import clean_generated_sql
from sql_prompt import SQL_PROMPT
from educational_data_context import EDUCATIONAL_DATA_CONTEXT
from analysys_prompt import ANALYSIS_PROMPT
from perguntas_de_avaliacao import PERGUNTAS_DE_AVALIACAO

@st.cache_data
def generate_sql_cached(question):
    prompt_messages = sql_chain_prompt.format(question=question, history=[question.content for question in st.session_state.history.messages[-15:] if question.type == 'human'])
    response = db_chain.invoke(prompt_messages) 
    return response["result"] if response else "Analysis unavailable."
        
@st.cache_data
def analyze_data_cached(question, data_as_df):
    prompt_messages = analysis_prompt.format(data=data_as_df.to_csv(index=False), question=question, history=[question.content for question in st.session_state.history.messages[-15:]])
    response = llm_analysis.invoke(prompt_messages)
    return response.content if response else "Analysis unavailable."

API_KEY = os.environ["OPEN_AI_KEY"]
llm_text_2_sql = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY, temperature=0) 
llm_analysis = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY, temperature=.75, verbose=True) 

n_cidades_brasileiras = 5571

# Connect to the database
engine = create_engine('sqlite:///database.db') 
sql_database = SQLDatabase(engine=engine, view_support=True)

# Create SQL agent chain and prompt
db_chain = SQLDatabaseChain.from_llm(llm_text_2_sql, sql_database, 
                                     verbose=True, return_sql=True, 
                                     input_key="question")

sql_chain_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        SQL_PROMPT
    ),
    HumanMessagePromptTemplate.from_template(
        "Aqui está a nova pergunta: {question}"
    )
]).partial(
    dialect=sql_database.dialect,
    top_k=str(trunc(n_cidades_brasileiras/3)),
    db=sql_database,
    educational_data_context=EDUCATIONAL_DATA_CONTEXT
)

# Define analysis prompt
analysis_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        ANALYSIS_PROMPT
    ),
    HumanMessagePromptTemplate.from_template(
        "Here are the results from the SQL query in a csv file:\n\n{data}\n\n"
        "This is my current question: {question}\n\n"
        "Summarize the key insights found in this data."
    )
]).partial(educational_data_context=EDUCATIONAL_DATA_CONTEXT)


# Initialize memory in session state
if "history" not in st.session_state:
    st.session_state.history = ChatMessageHistory() # Change this to StreamlitChatMessageHistory

# Set Streamlit UI
st.title("Converse com o banco de dados de indicadores da educação brasileira")

# Capture user input
question = st.chat_input("Quantas escolas existem na cidade de São Paulo?")

#if question:
if st.button("Test questions"):
    for question in PERGUNTAS_DE_AVALIACAO:
        result = None
        generated_sql = ""
        sql_result_as_list_of_dict = []

        df = None
        st.session_state.history.add_message(BaseMessage(content=question, type="user", name="question")) 
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Analisando..."):
            try:
                # Generate SQL query
                result = generate_sql_cached(question)
                generated_sql = clean_generated_sql(result)
                
                # Save generated SQL to history
                st.session_state.history.add_message(BaseMessage(content=generated_sql, type="assistant", name="sql"))

                # Display generated SQL
                st.code(generated_sql, language="sql")

                # Execute the generated SQL query
                try:
                    sql_run_result = sql_database.run(generated_sql, include_columns=True) 
                    # Convert the result to a DataFrame
                    sql_result_as_list_of_dict = ast.literal_eval(sql_run_result) if isinstance(sql_run_result, str) else sql_run_result
                    df = pd.DataFrame(sql_result_as_list_of_dict)
                except: 
                    sql_run_result = '{}'
                    df = pd.DataFrame()
                    st.error(f"Erro ao executar a consulta SQL: {generated_sql}")

                # Display query results
                st.subheader("Resultados do banco de dados:")
                st.dataframe(df)

                analysis_text = analyze_data_cached(data_as_df=df, question=question)
                # Save analysis history
                st.session_state.history.add_message(BaseMessage(content=analysis_text, type="assistant", name="analysis")) 
                
                # To save on tokens, the data given is limited by the number of cities in Brasil. 
                # This should't be necessary due to top_n in the SQL chain, but :shrug:
                #st.session_state.history.add_message(BaseMessage(content=sql_result_as_list_of_dict, type="assistant", name="dataframe"))
                st.session_state.history.add_message(BaseMessage(
                    content={
                        df.to_csv(index=False, sep=";")
                    },
                    type="assistant",
                    name="dataframe"
                ))

                # Display AI response
                with st.chat_message("assistant"):
                    st.markdown("**Análise:**")
                    st.write(analysis_text)

            except Exception as e:
                with st.chat_message("assistant"):
                    st.error(f"Error: {str(e)}")

# Display database schema information
#if st.checkbox("Show Database Schema"):
with st.sidebar:
    # Display button to clear history
    if st.button("Limpar Histórico de Análises"):
        st.session_state.history.clear()

    with st.expander("Database Schema"):
        st.code(sql_database.get_table_info(), language="sql")

    # Display generated SQL history
    with st.expander("Show History"):
        for message in st.session_state.history.messages:
            role = "user" if message.type == "human" else "assistant"
            with st.chat_message(role):
                if message.name == "sql":
                    st.code(message.content, language="sql")
                elif message.name == "dataframe":
                    st.dataframe(message.content)
                else:
                    st.markdown(message.content)
        
if st.sidebar.button("Exportar Histórico"):
    # Create a structured list to store all conversations
    history_data = []
    
    # Organize messages by their 'name' attribute
    messages_by_name = {}
    for message in st.session_state.history.messages:
        if message.name:  # Ensure there's a name
            messages_by_name.setdefault(message.name, []).append(message.content)

    export_df = pd.DataFrame.from_dict(messages_by_name, orient="index").T 
    #dearlord
    export_df["dataframe"] = export_df["dataframe"].apply(lambda x: pd.read_csv(io.StringIO(x[0]), sep=";").to_markdown(index=False)) 

    # Convert to CSV
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button(
        label="Baixar Histórico CSV",
        data=csv_data,
        file_name="historico_consultas.csv",
        mime="text/csv"
    )
