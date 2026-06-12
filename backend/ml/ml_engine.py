import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier, XGBRegressor
from sklearn.preprocessing import LabelEncoder
import yaml
import os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.metrics import f1_score,mean_absolute_error,accuracy_score,mean_squared_error,roc_auc_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split, GridSearchCV



def load_config():
    with open("backend/config.yaml","r") as f:
        return yaml.safe_load(f)
    

#load processing data

def load_data(config):
    ticket_df=pd.read_csv(config["data"]["processed"]["ticket"])
    delay_df=pd.read_csv(config["data"]["processed"]["delay"])
    
    #just print the shape to confirm no error in loading the data 
    print(f"Ticket   : {ticket_df.shape}")
    print(f"Delay    : {delay_df.shape}")

    return ticket_df,delay_df



def get_ticket_column_types(df, target):
    # ordered columns — label encode
    label_cols = [
        "Holiday or Peak Season",   # Yes/No has no real order but binary fine
        "journey_month",            # already numeric
        "journey_dayofweek",        # already numeric
        "days_before_journey"       # already numeric
    ]

    
    onehot_cols = [
        "Class of Travel",
        "Quota",
        "Source Station",
        "Destination Station",
        "Train Type",
        "Special Considerations",
        "Seat Availability"
    ]

    
    numeric_cols = [
        col for col in df.columns
        if col not in label_cols
        and col not in onehot_cols
        and col != target
    ]

    return label_cols, onehot_cols, numeric_cols


def get_delay_column_types(df, target):
    # ordered
    label_cols = [
        "Season",
        "journey_month",
        "journey_dayofweek"
    ]

    # no-order categorical
    onehot_cols = [
        "Source",
        "Destination",
        "Run_frequency"
    ]

    # already numeric
    numeric_cols = [
        col for col in df.columns
        if col not in label_cols
        and col not in onehot_cols
        and col != target
    ]

    return label_cols, onehot_cols, numeric_cols

def build_preprocessor(label_cols,onehot_cols,numeric_cols):

    label_pipeline=Pipeline(steps=[('le',OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))])

    onehot_pipeline=Pipeline(steps=[("ohe",OneHotEncoder(handle_unknown='ignore'))])

    preprocessor=ColumnTransformer(transformers=[("label",label_pipeline,label_cols),("ohe",onehot_pipeline,onehot_cols),("numeric", "passthrough", numeric_cols)], sparse_threshold=0)

    return preprocessor
    # only the blue print is made , no real preprocessing is done here , the preprocessor will be fitted in the training function and then used for both train and test data to avoid data leakage

# training the classifer model
def train_classifier(tickect_df):

    config=load_config()
    target=config["features"]["ticket"]["target"]

    X=tickect_df.drop(columns=[target])
    y=tickect_df[target]
    use_cols=config["features"]["ticket"]["use"]
    X=X[use_cols]

    label_cols,onehot_cols,numeric_cols=get_ticket_column_types(X,target)
    preprocessor=build_preprocessor(label_cols=label_cols,onehot_cols=onehot_cols,numeric_cols=numeric_cols)

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

    pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", XGBClassifier(random_state=42, eval_metric="logloss"))])

    param_grid = {
        "model__n_estimators"  : [100, 200, 300],
        "model__max_depth"     : [3, 4, 6],
        "model__learning_rate" : [0.05, 0.1, 0.2],
    }
   
    grid = GridSearchCV(estimator=pipeline, param_grid=param_grid,
                        cv=5, scoring="f1", n_jobs=-1, verbose=1)

    grid.fit(X_train, y_train)

    print(f"\nBest Params : {grid.best_params_}")
    print(f"Best CV F1  : {grid.best_score_:.4f}")
   
    best_model  = grid.best_estimator_
    y_pred      = best_model.predict(X_test)
    y_pred_prob = best_model.predict_proba(X_test)[:, 1]

    print(f"\n--- Final Test Scores ---")
    print(f"F1 Score : {f1_score(y_test, y_pred):.4f}")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"AUC      : {roc_auc_score(y_test, y_pred_prob):.4f}")

    return best_model


def train_regressor(delay_df):
    config=load_config()
    target=config["features"]["delay"]["target"]

    X=delay_df.drop(columns=[target])
    y=delay_df[target]

    label_cols,onehot_cols,numeric_cols=get_delay_column_types(X,target)
    preprocessor=build_preprocessor(label_cols=label_cols,onehot_cols=onehot_cols,numeric_cols=numeric_cols)

   
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

    pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", XGBRegressor(random_state=42))])

   
    param_grid = {
        "model__n_estimators"  : [100, 200, 300],
        "model__max_depth"     : [3, 4, 6],
        "model__learning_rate" : [0.05, 0.1, 0.2],
    }


    grid = GridSearchCV(estimator=pipeline, param_grid=param_grid,
                        cv=5, scoring="neg_mean_absolute_error", n_jobs=-1, verbose=1)

    grid.fit(X_train, y_train)

    print(f"\nBest Params : {grid.best_params_}")
    print(f"Best CV MAE : {-grid.best_score_:.4f}")

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)

    print(f"\n--- Final Test Scores ---")
    print(f"MAE : {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"MSE : {mean_squared_error(y_test, y_pred):.4f}")

    return best_model

def save_models(classifier, regressor, config):
    os.makedirs("backend/ml", exist_ok=True)

    joblib.dump(classifier, config["models"]["classifier"]["path"])
    joblib.dump(regressor,  config["models"]["regressor"]["path"])

    
    print(f"Classifier → {config['models']['classifier']['path']}")
    print(f"Regressor  → {config['models']['regressor']['path']}")



if __name__ == "__main__":
    config = load_config()

    ticket_df, delay_df = load_data(config)

    classifier = train_classifier(ticket_df)
    regressor  = train_regressor(delay_df)

    save_models(classifier, regressor, config)

    print("\nml_engine.py complete ✅")