from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import pickle

df = pd.read_csv("spectrum_db.csv", skipinitialspace=True)
# print(df.head())

X = df.iloc[:, 0:6]
# print(X.head())

y = df.select_dtypes(include=[object])
# print(y.type.unique())
le = preprocessing.LabelEncoder()
y = y.apply(le.fit_transform)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)
learn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(10, 100, 50, 100, 100, 10), max_iter=1000, verbose=True)
mlp.fit(X_train, y_train.values.ravel())

predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions, zero_division=0))
pickle.dump(mlp, open("mlmodel.mdl", "wb"))