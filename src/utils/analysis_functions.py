import pandas as pd
import seaborn as sns
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)


def summary_by_columns(df):
    """
    Generates a summary of each column in the provided DataFrame.

    The summary includes the data type, number of missing values, number of unique values,
    and number of duplicate values for each column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to summarize.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the summary information for each column.
    """
    # Create an empty DataFrame to store the summary
    summary_df = pd.DataFrame(
        columns=['Column', 'Data Type', 'Missing Values', 'Unique Values', 'Duplicates'])

    # Loop through each column in the DataFrame
    for col in df.columns:
        data_type = df[col].dtype
        missing_values = df[col].isna().sum()
        num_unique_values = df[col].nunique()
        num_duplicates = df[col].duplicated().sum()

        # Add the results to the summary DataFrame
        row_summary = pd.DataFrame({
            'Column': [col],
            'Data Type': [data_type],
            'Missing Values': [missing_values],
            'Unique Values': [num_unique_values],
            'Duplicates': [num_duplicates],
            'Missing Values (%)': [round((missing_values / df.shape[0]) * 100, 2)]
        })

        # Concatenate the row summary to the summary DataFrame
        summary_df = pd.concat([summary_df, row_summary], ignore_index=True)

    return summary_df


def plot_correlation_matrix(df):
    """
    Plots a correlation heatmap for numeric columns in the given DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.

    The function selects numeric columns, calculates their correlation matrix, 
    and plots a heatmap to visualize correlations. Any exceptions encountered 
    during execution are logged as errors.
    """
    try:
        df_numerics = df.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = df_numerics.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True,
                    cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Mapa de Correlación')
        plt.show()
    except Exception as e:
        logging.error(f"The following error occurred: {e}")
