"""
Data Cleaning Module

This module provides functions for parsing grace and condone 
entries in a DataFrame and cleaning data.

"""
import pandas as pd


def parse_grace_condone(entry: str) -> int:
    """
    Parse and calculate the adjusted value for entries with '*' or '@'.

    Parameters:
    - entry (str): A string containing a numeric part and a special character
    '*' or '@' indicating grace or condone respectively.

    Returns:
    - int: The adjusted numeric value based on the grace or condone entry.

    Explanation:
    This function takes an entry as a string and checks if it contains '*' or '@'.
    If '*' is present, it splits the entry into numeric parts and returns the sum of both parts.
    If '@' is present, it splits the entry into numeric parts and returns the sum of both parts.
    If no special characters are present, it returns the original value converted to an integer.

    Example:
    >>> parse_grace_condone("11*5")
    16

    """
    
    if isinstance(entry, str):
        # Check if the entry contains '*'
        if "*" in entry:
            parts = entry.split("*")
            # Extract the numeric part and multiply by the grace factor
            return int(parts[0]) + int(parts[1])
        # Check if the entry contains '@'
        if "@" in entry:
            parts = entry.split("@")
            # Extract the numeric part and add the condoned value
            return int(parts[0]) + int(parts[1])
        if 'AB' in entry or 'CC' in entry:
            return entry
        return int(entry)

    # If no special characters, return the original value
    return entry


def clean_data(file: str) -> pd.DataFrame:
    """
    Clean data in a DataFrame by replacing 'AB' with 0 for absent
    students and 'CC' with 0 for copy case.

    Parameters:
    - file (str): The file path to the CSV file containing the data.

    Returns:
    - pd.DataFrame: A cleaned DataFrame with 'AB' and 'CC' replaced with 0.

    Explanation:
    This function reads a CSV file into a DataFrame and replaces 'AB' with 0 for absent students
    and 'CC' with 0 for copy case entries. The cleaned DataFrame is then returned.

    Example:
    >>> pd.read_csv("data.csv")
         Name  Subject1  Subject2
    0  Student1        80        AB
    1  Student2        CC        75
    2  Student3        90        85
    3  Student4        79@1      85
    4  Student5        35*5      45

    >>> # After applying clean data
    >>> clean_data("data.csv")
         Name  Subject1  Subject2
    0  Student1        80         0
    1  Student2         0        75
    2  Student3        80        85
    3  Student4        80        85
    4  Student5        40        45

    """
    df = pd.read_csv(file)

    subject_columns = [col for col in df.columns if "BIT" in col]
    df = df[["StudentId", "StudentName"] + subject_columns]
    df[subject_columns] = df[subject_columns].map(parse_grace_condone)

    absent_students = df.apply(lambda row: "AB" in row.values, axis=1)
    df.loc[absent_students] = df.loc[absent_students].replace("AB", 0)

    copy_case = df.apply(lambda row: "CC" in row.values, axis=1)
    df.loc[copy_case] = df.loc[copy_case].replace("CC", 0)
    return df
