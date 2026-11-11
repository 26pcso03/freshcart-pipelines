from sklearn.metrics import classification_report, confusion_matrix

def export_data(df, *args, **kwargs):
    print(confusion_matrix(df['target'], df['prediction']))
    print(classification_report(df['target'], df['prediction']))
