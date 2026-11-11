from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def transform(df, *args, **kwargs):
    features = [c for c in df.columns if c not in ['target', 'split']]
    train_df, test_df = df[df['split'] == 'train'], df[df['split'] == 'test'].copy()
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(train_df[features], train_df['target'])
    test_df['prediction'] = clf.predict(test_df[features])
    test_df['accuracy'] = accuracy_score(test_df['target'], test_df['prediction'])
    return test_df
