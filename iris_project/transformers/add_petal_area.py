def transform(df, *args, **kwargs):
    df = df.copy()
    df['petal_area'] = df['petal length (cm)'] * df['petal width (cm)']
    return df

def test_output(output, *args) -> None:
    assert 'petal_area' in output.columns and (output['petal_area'] > 0).all()
