import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_curve

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score

from scipy.stats import ttest_ind

# =========================================
# 2. Load dataset which was integrated
# =========================================
df = pd.read_csv("FINAL_IOT_DATASET.csv")

print("Original Shape:", df.shape)

# 🔥 Reduce size
if len(df) > 200000:
    df = df.sample(n=200000, random_state=42)
    print("Reduced Shape:", df.shape)

# =========================================
# 3.  LABEL COLUMN
# =========================================
print("Columns:", df.columns)

if 'Label' in df.columns:
    df.rename(columns={'Label': 'Attack_Type'}, inplace=True)
elif 'label' in df.columns:
    df.rename(columns={'label': 'Attack_Type'}, inplace=True)
elif 'Attack' in df.columns:
    df.rename(columns={'Attack': 'Attack_Type'}, inplace=True)
elif 'Class' in df.columns:
    df.rename(columns={'Class': 'Attack_Type'}, inplace=True)

if 'Attack_Type' not in df.columns:
    raise Exception("❌ No label column found!")

# =========================================
# 4. DATA CLEANING
# =========================================
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# =========================================
# 5. ENCODING 
# =========================================
if df['Attack_Type'].dtype != 'int64' and df['Attack_Type'].dtype != 'float64':
    le = LabelEncoder()
    df['Attack_Type'] = le.fit_transform(df['Attack_Type'])

# =========================================
# 6. KEEP NUMERIC ONLY 
# =========================================
df_numeric = df.select_dtypes(include=[np.number])

if 'Attack_Type' not in df_numeric.columns:
    raise Exception("❌ Attack_Type missing after encoding!")

# =========================================
# 7. SPLIT DATA
# =========================================
X = df_numeric.drop('Attack_Type', axis=1)
y = df_numeric['Attack_Type']

# =========================================
# 8. SCALING
# =========================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================================
# 9. PCA
# =========================================
pca = PCA(n_components=min(10, X_scaled.shape[1]))
X_pca = pca.fit_transform(X_scaled)

print("After PCA:", X_pca.shape)

# =========================================
# 10. DISCRETIZATION
# =========================================
try:
    df['Binned_Feature'] = pd.cut(df[X.columns[0]], bins=5)
except:
    print("Discretization skipped")

# =========================================
# 11. EDA
# =========================================
print(df.describe())

sns.countplot(x='Attack_Type', data=df)
plt.title("Class Distribution")
plt.show()

plt.figure(figsize=(8,6))
sns.heatmap(df_numeric.sample(5000).corr(), cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

# =========================================
# 12. FEATURE SELECTION
# =========================================
selector = SelectKBest(chi2, k=min(10, X_scaled.shape[1]))
X_selected = selector.fit_transform(abs(X_scaled), y)

# =========================================
# 13. TRAIN TEST SPLIT
# =========================================
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.3, random_state=42
)

# =========================================
# 14. MODELS + CONFUSION MATRIX
# =========================================
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "KNN": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": GaussianNB(),
    "Random Forest": RandomForestClassifier(n_estimators=50)
}

accuracies = {}

for name, model in models.items():
    print(f"\n===== {name} =====")
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = model.score(X_test, y_test)
    accuracies[name] = acc
    
    print("Accuracy:", acc)
    
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(name + " Confusion Matrix")
    plt.show()
    
    print(classification_report(y_test, y_pred))

# =========================================
# 15. ACCURACY GRAPH
# =========================================
plt.figure()
plt.bar(accuracies.keys(), accuracies.values())
plt.xticks(rotation=30)
plt.title("Model Comparison")
plt.show()

# =========================================
# 16. ROC CURVE
# =========================================
try:
    y_binary = (y > 0).astype(int)

    X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
        X_selected, y_binary, test_size=0.3
    )

    rf = RandomForestClassifier()
    rf.fit(X_train_b, y_train_b)

    y_prob = rf.predict_proba(X_test_b)[:,1]

    fpr, tpr, _ = roc_curve(y_test_b, y_prob)

    plt.figure()
    plt.plot(fpr, tpr)
    plt.title("ROC Curve")
    plt.show()
except:
    print("ROC skipped")

# =========================================
# 17. T-TEST
# =========================================
try:
    feature = X.columns[0]

    class0 = df[df['Attack_Type']==0][feature]
    class1 = df[df['Attack_Type']==1][feature]

    print("T-Test:", ttest_ind(class0, class1))
except:
    print("T-test skipped")

# =========================================
# 18. CLUSTERING
# =========================================
try:
    kmeans = KMeans(n_clusters=3)
    labels_k = kmeans.fit_predict(X_pca)
    print("KMeans Score:", silhouette_score(X_pca, labels_k))

    db = DBSCAN()
    labels_db = db.fit_predict(X_pca)
    print("DBSCAN clusters:", len(set(labels_db)))

    agg = AgglomerativeClustering(n_clusters=3)
    labels_agg = agg.fit_predict(X_pca)
    print("Hierarchical Score:", silhouette_score(X_pca, labels_agg))
except:
    print("Clustering skipped")

print("\n FINAL PIPELINE RUN SUCCESSFUL")
