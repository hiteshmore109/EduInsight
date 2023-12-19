import pandas as pd


def calculate_credits(marks):
    return pd.cut(
        marks,
        bins=[0, 40, 45, 50, 55, 60, 70, 80, 101],
        labels=[0, 4, 5, 6, 7, 8, 9, 10],
        right=False,
    )


def calculate_practical_percentage(marks):
    return marks // 0.5


# def get_combined_sgpa(sem1, sem2, sem3):
#     df = pd.DataFrame()
#     df['Combined name'] = sem1['Combined name']
#     semesters = ['Sem1', 'Sem2', 'Sem3']
#     sgpa_dfs = [sem1, sem2, sem3]
#     for semester, sgpa_df in zip(semesters, sgpa_dfs):
#         df = pd.merge(df, sgpa_df[['Combined name', 'GPA']], on='Combined name', how='outer')
#         df = df.rename(columns={'GPA': semester})
#     df.iloc[:, 1:] = df.iloc[:, 1:].map(lambda x: 0 if x < 4 else x)
#     df[semesters] = df[semesters].fillna(df[semesters].median())
#     return df


def get_combined_sgpa(*semesters: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["Combined name"] = semesters[0]["Combined name"]

    semester_names = [f"Sem{i+1}" for i in range(len(semesters))]

    for semester, semester_name in zip(semesters, semester_names):
        df = pd.merge(
            df, semester[["Combined name", "GPA"]], on="Combined name", how="inner"
        )
        df = df.rename(columns={"GPA": semester_name})

    df.iloc[:, 1:] = df.iloc[:, 1:].map(lambda x: 0 if x < 4 else x)
    df[semester_names] = df[semester_names].fillna(df[semester_names].median())

    return df


def get_sgpa(sem_data: pd.DataFrame) -> pd.DataFrame:
    subject_columns = [col for col in sem_data.columns if col.endswith(("Int", "Ext"))]
    practical_columns = [
        col for col in sem_data.columns if col.endswith(("Pint", "Prac"))
    ]
    sem_data[subject_columns] = sem_data[subject_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    sem_data[practical_columns] = sem_data[practical_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    credits_df = pd.DataFrame()

    for practical_column in practical_columns:
        practical_name = practical_column.split()[0]
        practical_name += "Prac"
        total_marks = (
            sem_data[practical_column]
            + sem_data[practical_column.replace("Prac", "Pint")]
        )
        total_marks = calculate_practical_percentage(total_marks)
        gpa = calculate_credits(total_marks)
        credits_df[practical_name] = gpa

    for subject_column in subject_columns:
        subject_name = subject_column.split()[0]
        total_marks = (
            sem_data[subject_column] + sem_data[subject_column.replace("Ext", "Int")]
        )
        gpa = calculate_credits(total_marks)
        credits_df[subject_name] = gpa

    credits_df.fillna(0, inplace=True)
    credits_df = credits_df.apply(pd.to_numeric)
    total_credits = credits_df.sum(axis=1)
    gpa = total_credits / 10
    credits_df["GPA"] = gpa
    credits_df["Combined name"] = sem_data["Combined name"]
    return credits_df
