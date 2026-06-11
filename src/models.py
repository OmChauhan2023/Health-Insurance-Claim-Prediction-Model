import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

def get_lightgbm_model(random_state=42):
    # Optuna-tuned parameters on new 109 feature set (500 iterations)
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'num_leaves': 28,
        'learning_rate': 0.010040010738299996,
        'n_estimators': 871,
        'max_depth': 8,
        'min_child_samples': 123,
        'reg_alpha': 0.27925954058789804,
        'reg_lambda': 0.5765421794757126,
        'feature_fraction': 0.5824426060495409,
        'bagging_fraction': 0.7393105058690916,
        'bagging_freq': 1,
        'min_gain_to_split': 0.8001097360401972,
        'random_state': random_state,
        'verbose': -1
    }
    return lgb.LGBMClassifier(**params)

def get_xgboost_model(random_state=42):
    # Optuna-tuned parameters on new 109 feature set (500 iterations)
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 4,
        'learning_rate': 0.02123178809883266,
        'n_estimators': 519,
        'subsample': 0.894325792449818,
        'colsample_bytree': 0.7692629157015227,
        'min_child_weight': 17,
        'reg_alpha': 0.03788798831050035,
        'reg_lambda': 0.01564247490927308,
        'gamma': 0.6043964592192503,
        'random_state': random_state,
        'tree_method': 'hist'
    }
    return xgb.XGBClassifier(**params)

def get_catboost_model(random_state=42):
    # Optuna-tuned parameters — Val Gini: 0.2848
    params = {
        'iterations': 854,
        'learning_rate': 0.010465232610199155,
        'depth': 8,
        'l2_leaf_reg': 7.717523098478614,
        'border_count': 102,
        'random_seed': random_state,
        'verbose': False,
        'eval_metric': 'AUC',
        'early_stopping_rounds': 50
    }
    return CatBoostClassifier(**params)

def get_all_models(random_state=42):
    return {
        'LightGBM': get_lightgbm_model(random_state),
        'XGBoost': get_xgboost_model(random_state),
        'CatBoost': get_catboost_model(random_state)
    }
