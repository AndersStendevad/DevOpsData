#!/usr/bin/env python3

import pandas as pd
import sqlite3

sqlite_conn = sqlite3.connect("minitwit.db")


def load_users():
    df = pd.read_sql_query("SELECT * from user;", sqlite_conn)
    print(df.head())


def load_messages():
    df = pd.read_sql_query("SELECT * from message;", sqlite_conn)
    print(df.head())


def load_followers():
    df = pd.read_sql_query("SELECT * from follower;", sqlite_conn)
    print(df.head())


def main():
    load_users()
    load_messages()
    load_followers()


if __name__ == "__main__":
    main()
