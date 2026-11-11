from sklearn.datasets import load_iris

def load_data(*args, **kwargs):
    return load_iris(as_frame=True).frame

def test_output(output, *args) -> None:
    assert output is not None and len(output) == 150
