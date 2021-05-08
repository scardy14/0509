# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1140bn4DhVZTtowrDV4wY7j4zx16-pP34
"""

from sklearn.datasets import fetch_openml
mnist = fetch_openml('mnist_784',version=1)

from sklearn.model_selection import train_test_split

X_train_val, X_test, y_train_val, y_test = train_test_split(mnist.data,mnist.target,test_size=10000, random_state=42)
X_train,X_val,y_train,y_val = train_test_split(X_train_val,y_train_val,test_size=10000,random_state=42)

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier

rnd_clf = RandomForestClassifier(n_estimators=10,random_state=42)
ext_clf = ExtraTreesClassifier(n_estimators=10, random_state=42)
svm_clf = LinearSVC(max_iter=10000,random_state=42)
mlp_clf = MLPClassifier(random_state=42)

from sklearn.metrics import accuracy_score

#여러개의 학습기를 한 번에 훈련시킨다.
models = [rnd_clf,ext_clf,svm_clf,mlp_clf]

for model in models:
    print("훈련 :",model)
    model.fit(X_train,y_train)

#학습기들의 결과값을 한 번에 본다.
for model in models:
    y_pred = model.predict(X_val)
    print("정확도 :",accuracy_score(y_val,y_pred))

from sklearn.ensemble import VotingClassifier

named_models = [
    ("RandomForest" , rnd_clf),
    ("ExtraTree" , ext_clf),
    ("LinearSVM" , svm_clf),
    ("MLP" , mlp_clf),
]

voting_clf = VotingClassifier(named_models)

voting_clf.fit(X_train,y_train)

voting_clf.score(X_val,y_val)

[model.score for model in voting_clf.estimators_ ]

# SVM제거
voting_clf.set_params(LinearSVM=None)

voting_clf.estimators_

#SVM제거2
del voting_clf.estimators_[2]

voting_clf.score(X_val,y_val)

# 간접투표 
# 기존에 훈련을 했었으므로  Hard -> soft 바꾸기

voting_clf.voting = 'soft'

# 설정을 변경했으니 다시 평가해보기
voting_clf.score(X_val,y_val)

# 단독의 학습 및 분류보다 나은 결과를 보여준다.
voting_clf.score(X_test,y_test)

[model.score(X_test,y_test) for model in voting_clf.estimators_]