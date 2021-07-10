#Path Configs
DATASET_PATH = "./dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Train"
TESTSET_PATH = "./dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test"
TARGET_PATH = "./dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test/UCSDped1.m"
MODEL_PATH = "./models"
RESULT_PATH = "./results"
SINGLE_TEST_CASE_NAME = "Test036"
CACHE_PATH = "cache"
USE_SINGLE_TEST_CASE = False
SINGLE_FRAME_EVALUATOR = False

#Model Configs
TESTSET_STRUCTURE = "dict" # ["dict", "array_seq"]
MODEL_NAME = "perfect_convolutional_autoencoder" # ['lstm_autoencoder', 'autoencoder', 'deep_autoencoder', 'convolutional_autoencoder', 'perfect_convolutional_autoencoder']
OPTIMIZER = "adam" # ['adam','sgd','adagrad']
LOSS = "mean_squared_error" # ['mean_squared_error', 'binary_crossentropy'], default='mean_squared_error')
RELOAD_DATASET = True
RELOAD_TESTSET = True
RELOAD_MODEL = True
RETRAIN_MODEL = True
USE_OPTICAL_FLOW = False
BATCH_SIZE = 512
EPOCHS = 100

#Other Configs
CALCULATE_THRESHOLD = False
DISPAY_OUTPUT = False
LOAD_RESULT_FROM_CACHE = False
THRESHOLD_SCALING_FACTOR = 1# 0.875
THRESHOLD_VALUE = 51#51 #0.003112044614227831 # 11800.636563585069# 0.003883616714276072 #0.007268916599438799 #0.005192083285313428
IMAGE_SHAPE_X = 128
IMAGE_SHAPE_Y = 128
USE_BINARIZED_OPTICAL_FLOW = False
SUBTRACT_BACKGROUND = False
FIND_BEST_THRESHOLD = False

CALCULATE_THRESHOLD = FIND_BEST_THRESHOLD = LOAD_RESULT_FROM_CACHE = False
