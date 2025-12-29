# Dataset Analysis Module
# A comprehensive module for data exploration, analysis, and visualization.
Includes functions for loading data, statistical analysis, and generating insights.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List, Dict, Any
import warnings

warnings.filterwarnings('ignore')

# Configure visualization defaults
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class DatasetAnalyzer:
    """
    A class for comprehensive data analysis and exploration.
    """
    
    def __init__(self, filepath: str, **kwargs):
        """
        Initialize the analyzer with a dataset.
        
        Args:
            filepath (str): Path to the data file (CSV, Excel, or Parquet)
            **kwargs: Additional arguments to pass to pandas read function
        """
        self.filepath = filepath
        self.df = None
        self.load_data(**kwargs)
    
    def load_data(self, **kwargs) -> pd.DataFrame:
        """Load data from various file formats."""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath, **kwargs)
            elif self.filepath.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(self.filepath, **kwargs)
            elif self.filepath.endswith('.parquet'):
                self.df = pd.read_parquet(self.filepath, **kwargs)
            else:
                raise ValueError("Unsupported file format. Use CSV, Excel, or Parquet.")
            
            print(f"✓ Data loaded successfully. Shape: {self.df.shape}")
            return self.df
        
        except FileNotFoundError:
            print(f"✗ File not found: {self.filepath}")
            raise
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            raise
    
    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic information about the dataset."""
        info = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'duplicates': self.df.duplicated().sum(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        return info
    
    def display_summary(self) -> None:
        """Display a comprehensive summary of the dataset."""
        print("\n" + "="*60)
        print("DATASET SUMMARY".center(60))
        print("="*60)
        
        info = self.get_basic_info()
        
        print(f"\nShape: {info['shape'][0]} rows × {info['shape'][1]} columns")
        print(f"Memory Usage: {info['memory_usage']:.2f} MB")
        print(f"Duplicated Rows: {info['duplicates']}")
        
        print("\n" + "-"*60)
        print("COLUMN INFORMATION".center(60))
        print("-"*60)
        print(self.df.info())
        
        print("\n" + "-"*60)
        print("MISSING VALUES".center(60))
        print("-"*60)
        missing_df = pd.DataFrame({
            'Column': info['missing_values'].keys(),
            'Count': info['missing_values'].values(),
            'Percentage': info['missing_percentage'].values()
        })
        print(missing_df.to_string(index=False))
        
        print("\n" + "-"*60)
        print("STATISTICAL SUMMARY".center(60))
        print("-"*60)
        print(self.df.describe())
    
    def handle_missing_values(self, strategy: str = 'mean', 
                             threshold: float = 0.5) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            strategy (str): 'mean', 'median', 'forward_fill', or 'drop'
            threshold (float): Drop columns with missing % above this threshold
        
        Returns:
            pd.DataFrame: DataFrame with missing values handled
        """
        df_clean = self.df.copy()
        
        # Drop columns with too many missing values
        missing_percent = df_clean.isnull().sum() / len(df_clean)
        cols_to_drop = missing_percent[missing_percent > threshold].index
        df_clean.drop(columns=cols_to_drop, inplace=True)
        print(f"Dropped {len(cols_to_drop)} columns with >{threshold*100}% missing values")
        
        # Handle remaining missing values
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        
        if strategy == 'mean':
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
            df_clean[categorical_cols] = df_clean[categorical_cols].fillna(df_clean[categorical_cols].mode().iloc[0])
        
        elif strategy == 'median':
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
            df_clean[categorical_cols] = df_clean[categorical_cols].fillna(df_clean[categorical_cols].mode().iloc[0])
        
        elif strategy == 'forward_fill':
            df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')
        
        elif strategy == 'drop':
            df_clean = df_clean.dropna()
        
        print(f"✓ Missing values handled using '{strategy}' strategy")
        return df_clean
    
    def get_outliers(self, column: str, method: str = 'iqr') -> pd.Series:
        """
        Identify outliers in a column.
        
        Args:
            column (str): Column name
            method (str): 'iqr' or 'zscore'
        
        Returns:
            pd.Series: Boolean series indicating outliers
        """
        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = (self.df[column] < (Q1 - 1.5 * IQR)) | (self.df[column] > (Q3 + 1.5 * IQR))
        
        elif method == 'zscore':
            z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
            outliers = z_scores > 3
        
        return outliers
    
    def correlate_features(self) -> pd.DataFrame:
        """Calculate correlation matrix for numeric features."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr()
    
    def plot_correlation_matrix(self, figsize: Tuple[int, int] = (12, 10)) -> None:
        """Plot correlation matrix heatmap."""
        corr = self.correlate_features()
        plt.figure(figsize=figsize)
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_distributions(self, columns: List[str] = None, figsize: Tuple[int, int] = (15, 10)) -> None:
        """Plot distributions of specified columns."""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()[:6]
        
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()
        
        for idx, col in enumerate(columns):
            if col in self.df.columns:
                axes[idx].hist(self.df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
                axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
        
        for idx in range(len(columns), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        plt.show()
    
    def plot_boxplots(self, columns: List[str] = None, figsize: Tuple[int, int] = (15, 10)) -> None:
        """Plot boxplots for outlier detection."""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()[:6]
        
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()
        
        for idx, col in enumerate(columns):
            if col in self.df.columns:
                axes[idx].boxplot(self.df[col].dropna())
                axes[idx].set_title(f'Boxplot of {col}', fontweight='bold')
                axes[idx].set_ylabel(col)
        
        for idx in range(len(columns), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, output_file: str = 'analysis_report.txt') -> None:
        """Generate a comprehensive analysis report."""
        with open(output_file, 'w') as f:
            info = self.get_basic_info()
            
            f.write("="*80 + "\n")
            f.write("DATA ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Dataset: {self.filepath}\n")
            f.write(f"Shape: {info['shape'][0]} rows × {info['shape'][1]} columns\n")
            f.write(f"Memory Usage: {info['memory_usage']:.2f} MB\n")
            f.write(f"Duplicated Rows: {info['duplicates']}\n\n")
            
            f.write("COLUMNS:\n")
            for col in info['columns']:
                f.write(f"  - {col}\n")
            
            f.write("\nMISSING VALUES:\n")
            for col, count in info['missing_values'].items():
                pct = info['missing_percentage'][col]
                f.write(f"  {col}: {count} ({pct:.2f}%)\n")
            
            f.write("\nSTATISTICAL SUMMARY:\n")
            f.write(self.df.describe().to_string())
        
        print(f"✓ Report saved to {output_file}")


def main():
    """Example usage of DatasetAnalyzer."""
    print("Dataset Analysis Module")
    print("Use DatasetAnalyzer class to analyze your data")
    print("\nExample:")
    print("  analyzer = DatasetAnalyzer('data.csv')")
    print("  analyzer.display_summary()")
    print("  analyzer.plot_distributions()")
    print("  analyzer.plot_correlation_matrix()")


if __name__ == '__main__':
    main()
