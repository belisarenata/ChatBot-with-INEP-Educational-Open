
import re


MAX_ANALYSIS_HISTORY = 10
def add_to_analysis_memory(st, question, generated_sql, results_df, analysis_text):
    """Formats and adds the analysis entry to the session state history, enforcing a maximum size."""
    
    # Format the new entry
    entry = (
        f"Pergunta: {question}\n"
        f"SQL Gerado:\n{generated_sql}\n"
        f"Resultados:\n{results_df.to_string(index=False)}\n"
        f"Análise:\n{analysis_text}"
    )
    
    # Append to history
    st.session_state.analysis_memory.add_ai_message(entry)
    
    # Maintain the maximum history size
    if len(st.session_state.analysis_memory) > MAX_ANALYSIS_HISTORY:
        st.session_state.analysis_memory.pop(0)  # Remove the oldest entry

# Function to clear the history
def clear_analysis_memory(st):
    st.session_state.analysis_memory = []
    st.success("Histórico de análises apagado!")

def clean_generated_sql(sql_query):
    match = re.search(r"with\s+", sql_query, re.IGNORECASE)
    if not match:
        match = re.search(r"select", sql_query, re.IGNORECASE)
    if match:
        # Keep everything from "SELECT" or "WITH" onward
        sql_query = sql_query[match.start():]  
    
    # Normalize whitespace
    sql_query = re.sub(r"\s+", " ", sql_query).strip()
    sql_query = sql_query.replace("```", "")
    return sql_query

