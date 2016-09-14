import sys
sys.dont_write_btyecode = True


# management
project_path = [p for p in sys.path if p.endswith('privacy_sharing')][0]+'/'  # auto. dont change

# model
# model = ['camel-1.6', 'xerces-1.4', 'ant-1.6', 'ant-1.7']
model = ['school']
record_attrs = ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3']

# parameters
test_set_ratio = 0.2
CLIFF_percentage = 0.3
Lace2_holder_number = 5
MORPH_alpha = 0.15
MORPH_beta = 0.35

predict_mode = 'REGRESSION'  # 'CLASSIFICATION_BIN' 'CLASSIFICATION_MUL'

