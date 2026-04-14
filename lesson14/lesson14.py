from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from lesson14.Untitled1 import ezberci_model, mentiqli_model, test_accuracy_mentiqli

X,y=make_classification(n_samples=100,n_features=20,random_state=42)

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)


ezberci_model=DecisionTreeClassifier(max_depth=None,random_state=42)
ezberci_model.fit(X_train,y_train)

train_accuracy_ezberci=accuracy_score(y_train,ezberci_model.predict(X_train))
test_accuracy_ezberci=accuracy_score(y_test,ezberci_model.predict(X_test))

mentiqli_model=DecisionTreeClassifier(max_depth=4,random_state=42)
mentiqli_model.fit(X_train,y_train)

train_accuracy_mentiqli=accuracy_score(y_train,mentiqli_model.predict(X_train))
test_accuracy_mentiqli=accuracy_score(y_test,mentiqli_model.predict(X_test))

print(train_accuracy_ezberci)
print(train_accuracy_mentiqli)
print(test_accuracy_ezberci)
print(test_accuracy_mentiqli)