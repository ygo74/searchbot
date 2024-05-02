# https://github.com/microsoft/autogen/blob/main/notebook/agentchat_logging.ipynb

import sqlite3

import pandas as pd

def get_log(dbname="logs.db", table="chat_completions"):

    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data


def str_to_dict(s):
    import json
    return json.loads(s)


def parse_detailed_logs(log_data):
    log_data_df = pd.DataFrame(log_data)

    log_data_df["total_tokens"] = log_data_df.apply(
        lambda row: str_to_dict(row["response"])["usage"]["total_tokens"], axis=1
    )

    log_data_df["request"] = log_data_df.apply(lambda row: str_to_dict(
        row["request"])["messages"][0]["content"], axis=1)

    log_data_df["response"] = log_data_df.apply(
        lambda row: str_to_dict(row["response"])["choices"][0]["message"]["content"], axis=1
    )

    return log_data_df

def write_detailed_logs(log_data_df):

    print(log_data_df.to_string(index=False))

def write_summarized_logs(log_data_df, logging_session_id):
    # Sum totoal tokens for all sessions
    total_tokens = log_data_df["total_tokens"].sum()

    # Sum total cost for all sessions
    total_cost = log_data_df["cost"].sum()

    # Total tokens for specific session
    session_tokens = log_data_df[log_data_df["session_id"] == logging_session_id]["total_tokens"].sum()
    session_cost = log_data_df[log_data_df["session_id"] == logging_session_id]["cost"].sum()

    print("Total tokens for all sessions: " + str(total_tokens) + ", total cost: " + str(round(total_cost, 4)))
    print(
        "Total tokens for session "
        + str(logging_session_id)
        + ": "
        + str(session_tokens)
        + ", cost: "
        + str(round(session_cost, 4))
    )