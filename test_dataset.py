import pandas as pd
from dataset import DatasetAnalyzer


def test_fill_numeric_only_csv(tmp_path):
    path = tmp_path / 'numbers.csv'
    path.write_text('a,b\n1,2\n,3\n')
    cleaned = DatasetAnalyzer(str(path)).handle_missing_values()
    assert cleaned['a'].tolist() == [1, 1]
    assert not cleaned.isna().any().any()
