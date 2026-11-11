from sklearn.model_selection import train_test_split
import pandas as pd

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(func): return func
    def test(func): return func


@transformer
def transform(df, *args, **kwargs):
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['target']
    )
    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df['split'] = 'train'
    test_df['split'] = 'test'
    return pd.concat([train_df, test_df], ignore_index=True)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert 'split' in output.columns, 'Missing split column'
