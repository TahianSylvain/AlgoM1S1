import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Charger le dataset
df = pd.read_csv("tic_tac_toe_dataset.csv")

# Séparer les features (X) et la cible (y)
X = df[[f"cell_{i}" for i in range(9)]]   # colonnes : cell_0 à cell_8
y = df["label"]                           # colonne cible

# Découpage entraînement / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèle KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Prédiction
y_pred = knn.predict(X_test)

# Résultat
print("Précision du modèle KNN :", accuracy_score(y_test, y_pred))