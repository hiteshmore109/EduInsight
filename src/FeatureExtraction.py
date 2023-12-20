"""
Converting the cleaned data into features
"""
import pandas as pd


def calculate_credits(marks):
    """
    Assigns credit values based on a given set of marks using predefined bins and labels.

    Parameters:
    - marks (array-like): An array or list containing numerical values representing student marks.

    Returns:
    - pandas.Series: A Pandas Series object containing credit
    values corresponding to the input marks.

    Explanation:
    This function categorizes input marks into predefined bins
    and assigns credit values accordingly. The bins and labels are set
    based on common grading ranges. The returned Pandas Series provides a
    convenient mapping between input marks and their corresponding credit values.

    Example:
    >>> marks = [35, 42, 58, 70, 90]
    >>> calculate_credits(marks)
    0    0
    1    6
    2    8
    3    9
    4    10
    dtype: category
    Categories (7, int64): [0 < 4 < 5 < 6 < 7 < 8 < 9 < 10]

    Note:
    - Bins: [0, 40, 45, 50, 55, 60, 70, 80, 101]
    - Labels: [0, 4, 5, 6, 7, 8, 9, 10]
    - The 'right' parameter is set to False, indicating that the intervals are left-closed.
    """
    return pd.cut(
        marks,
        bins=[0, 40, 45, 50, 55, 60, 70, 80, 101],
        labels=[0, 4, 5, 6, 7, 8, 9, 10],
        right=False,
    )


def calculate_practical_percentage(marks: int) -> int:
    """
    Calculate practical percentage based on provided marks.

    Parameters:
    - marks (numeric): A numerical value representing the practical marks.

    Returns:
    - numeric: The practical percentage calculated by dividing the input marks by 0.5.

    Explanation:
    This function calculates the practical percentage based on a simple division of
    the provided marks by 0.5.\n
    It is assumed that the input marks are given on a scale where each unit
    corresponds to 0.5 percentage points.\n
    Only applicable when the marks are given out off 50

    Example:
    >>> practical_marks = 15
    >>> calculate_practical_percentage(practical_marks)
    30.0

    Note:
    - The division by 0.5 is used under the assumption that
    marks provided are out of 50.

    """
    return marks // 0.5


def get_combined_sgpa(*semesters: pd.DataFrame) -> pd.DataFrame:
    """
    Combine SGPA data from multiple semesters into a single DataFrame.

    Parameters:
    - *semesters (pd.DataFrame): Variable-length argument list of DataFrames,
    each representing SGPA data for a semester.

    Returns:
    - pd.DataFrame: A DataFrame containing the combined SGPA data with a common
    identifier "Combined name" and individual semester columns.

    Explanation:
    This function takes SGPA DataFrames from multiple semesters and combines
    them into a single DataFrame. The combination is based on a common
    identifier column "Combined name." The individual semester SGPA columns
    are named as "Sem1", "Sem2", etc.

    Example:
    >>> semester1_data = pd.DataFrame({"Combined name": ["Student1", "Student2"],
                                        "GPA": [3.5, 4.0]})
    >>> semester2_data = pd.DataFrame({"Combined name": ["Student1", "Student2"],
                                        "GPA": [4.0, 3.8]})
    >>> combined_sgpa = get_combined_sgpa(semester1_data, semester2_data)
    >>> print(combined_sgpa)
       Combined name  Sem1  Sem2
    0      Student1   0.0   4.0
    1      Student2   4.0   3.8

    Note:
    - SGPA values below 4 are replaced with 0 representing the the student is failing
    in the subject.
    - Missing SGPA values are filled with the median SGPA for the respective semester.

    """
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
    """
    Calculate SGPA based on semester data.

    Parameters:
    - sem_data (pd.DataFrame): A DataFrame containing semester-wise subject and practical marks.

    Returns:
    - pd.DataFrame: A DataFrame containing SGPA values for subjects, practicals, and an overall GPA.

    Explanation:
    This function takes semester-wise data containing subject and practical marks,
    calculates SGPA for each,
    and computes an overall GPA. It utilizes helper functions
    'calculate_practical_percentage' and 'calculate_credits'.

    Example:
    >>> semester_data = pd.DataFrame({
    ...     'Combined name': ['Student1', 'Student2'],
    ...     'Subject1 Ext': [50, 58],
    ...     'Subject1 Int': [20, 25],
    ...     'Practical1 Pint': [15, 18],
    ...     'Practical1 Prac': [25, 30],
    ...     #Addition Subjects and practical marks
    ...     'Subject5 Ext': [56, 48],
    ...     'Subject5 Int': [20, 25],
    ...     'Practical5 Pint': [15, 18],
    ...     'Practical5 Prac': [25, 30]
    ... })
    >>> sgpa_data = get_sgpa(semester_data)
    >>> print(sgpa_data)
       Practical1Prac  Subject1  ......... Practical5Prac  Subject5  GPA
       Combined name
    0              8.0       7.0 .........             8.0       5.6  1.5
          Student1
    1              9.0       8.0 .........             9.0       4.8  1.7
          Student2

    """
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
