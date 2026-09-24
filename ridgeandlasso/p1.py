from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load data and split
X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Scale features (required for regularized regression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. Fit Ridge (L2) and Lasso (L1) with built-in Cross-Validation
ridge = RidgeCV().fit(X_train, y_train)
lasso = LassoCV(random_state=42).fit(X_train, y_train)

# 4. Evaluate (R² Score)
print(f"Ridge R²: {ridge.score(X_test, y_test):.3f} (Best Alpha: {ridge.alpha_:.3f})")
print(f"Lasso R²: {lasso.score(X_test, y_test):.3f} (Best Alpha: {lasso.alpha_:.3f})")