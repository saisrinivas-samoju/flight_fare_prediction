import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


class BestModelFinder:
    def __init__(self, X, y, X_train, y_train, X_test, y_test):
        self.X = X
        self.y = y
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def dt_model(self):
        #         dt = DecisionTreeRegressor(criterion='friedman_mse', max_depth=10)
        param_grid = {"criterion": ["squared_error", "friedman_mse"], 'max_depth': [10, None]}
        # grid_dt = GridSearchCV(estimator=DecisionTreeRegressor(), param_grid=param_grid, cv=5, verbose=3)  # for reducing the training time
        grid_dt = GridSearchCV(estimator=DecisionTreeRegressor(), param_grid=param_grid, verbose=3)
        grid_dt.fit(self.X_train, self.y_train)
        return grid_dt.best_estimator_

    def rf_model(self):
        #         rf = RandomForestRegressor(min_samples_leaf=2, min_samples_split=10,n_estimators=300)
        param_grid = {'n_estimators': [300, 400], 'min_samples_split': [10, 12]}
        # grid_rf = GridSearchCV(estimator=RandomForestRegressor(min_samples_leaf=2), param_grid=param_grid, cv=5, verbose=3)  # for reducing the training time
        grid_rf = GridSearchCV(estimator=RandomForestRegressor(min_samples_leaf=2), param_grid=param_grid, verbose=3)
        grid_rf.fit(self.X_train, self.y_train)
        return grid_rf.best_estimator_

    def xgb_model(self):
        #         xgb = XGBRegressor(learning_rate=0.05, max_depth=5, n_estimators=500, reg_lambda=0.1)
        param_grid = {'max_depth': [5, 6], 'learning_rate': [0.01, 0.05], 'n_estimators': [500, 1000],
                      'reg_lambda': [0.001, 0.1]}
        # grid_xgb = GridSearchCV(estimator=XGBRegressor(), param_grid=param_grid, cv=5, verbose=3)  # for reducing the training time
        grid_xgb = GridSearchCV(estimator=XGBRegressor(), param_grid=param_grid, verbose=3)
        grid_xgb.fit(self.X_train, self.y_train)
        return grid_xgb.best_estimator_

    def get_best_model(self):

        # Decision Tree
        dt_model = self.dt_model()
        dt_preds = dt_model.predict(self.X_test)
        dt_score = r2_score(self.y_test, dt_preds)
        print("Decision tree model score:", dt_score)

        # Random Forest
        rf_model = self.rf_model()
        rf_preds = rf_model.predict(self.X_test)
        rf_score = r2_score(self.y_test, rf_preds)
        print("Random Forest Model Score:", rf_score)

        # XGBoost
        xgb_model = self.xgb_model()
        xgb_preds = xgb_model.predict(self.X_test)
        xgb_score = r2_score(self.y_test, xgb_preds)
        print("XGBoost model Score:", xgb_score)

        # Finding the best model with the best score
        scores = [dt_score, rf_score, xgb_score]
        model_idx = scores.index(max(scores))

        if model_idx == 0:
            print("Decision Tree Model is Chosen")
            dt_model.fit(self.X, self.y)
            return dt_model, "Decision Tree Regressor", dt_score
        elif model_idx == 1:
            print("Random Forest Model is Chosen")
            rf_model.fit(self.X, self.y)
            return rf_model, "Random Forest Regressor", rf_score
        else:
            print("XGBoost Model is Chosen")
            xgb_model.fit(self.X, self.y)
            return xgb_model, "XGBoost Regressor", xgb_score
