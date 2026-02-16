
model_features = [
    'EXT_SOURCE_1',
    'EXT_SOURCE_2',
    'EXT_SOURCE_3',
    'AMT_CREDIT',
    'AMT_ANNUITY',
    'PAYMENT_RATIO_MEAN',
    'POS_CNT_INSTALMENT_FUTURE_MEAN',
    'INST_NUM_INSTALMENT_NUMBER_COUNT',
    'PREV_CNT_PAYMENT_MEAN',
    'PREV_REFUSAL_RATE',
    'DAYS_EMPLOYED',
    'OWN_CAR_AGE',
    'CODE_GENDER'
]

categorical_features = ['CODE_GENDER']
numerical_features = [f for f in model_features if f not in categorical_features]
