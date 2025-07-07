from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def encoder_plateau(df):
    encoder = {"":0,"X":1,"0":-1}
    for i in range(9):
        df[f"case{i}"] = df[f"case{i}"].map(encoder)
    return df
    
#apple du fichier csv et tranformation de valeur en nombre
df = pd.read_csv("dataset_minimax_tictactoe.csv")
df = encoder_plateau(df)
    
#sépare les entrer (X) et (Y)
X = df[[f"case{i}"for i in range(9)]]
y = df["meilleur_coup"]
    
#entrainement de train/test
X_train , X_test ,y_train ,y_test = train_test_split(X,y, test_size = 0.2)
    
#création de knn
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
    
# Prédictions
y_pred = knn.predict(X_test)

# Précision
print("Précision du modèle KNN :", accuracy_score(y_test, y_pred))
    

