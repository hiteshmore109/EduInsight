import pandas as pd


def parse_grace_condone(entry):
    # Check if the entry contains '*'
    if "*" in entry:
        parts = entry.split("*")
        # Extract the numeric part and multiply by the grace factor
        return int(parts[0]) + int(parts[1])
    # Check if the entry contains '@'
    elif "@" in entry:
        parts = entry.split("@")
        # Extract the numeric part and add the condoned value
        return int(parts[0]) + int(parts[1])
    else:
        # If no special characters, return the original value
        return int(entry)


def clean_data(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)

    absent_students = df.apply(lambda row: "AB" in row.values, axis=1)
    df.loc[absent_students] = df.loc[absent_students].replace("AB", 0)

    copy_case = df.apply(lambda row: "CC" in row.values, axis=1)
    df.loc[copy_case] = df.loc[copy_case].replace("CC", 0)
    return df
