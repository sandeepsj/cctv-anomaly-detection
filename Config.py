#Path Configs
DATASET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Train"
TESTSET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test"
TARGET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test/UCSDped1.m"
MODEL_PATH = "/home/sandeepsj/cctv-anomaly-detection/models"
RESULT_PATH = "/home/sandeepsj/cctv-anomaly-detection/results"
SINGLE_TEST_CASE_NAME = "Test036"
CACHE_PATH = "cache"
USE_SINGLE_TEST_CASE = True
SINGLE_FRAME_EVALUATOR = False

#Model Configs
TESTSET_STRUCTURE = "dict" # ["dict", "array_seq"]
MODEL_NAME = "convolutional_autoencoder" # ['autoencoder', 'deep_autoencoder', 'convolutional_autoencoder']
OPTIMIZER = "adam" # ['adam','sgd','adagrad']
LOSS = "mean_squared_error" # ['mean_squared_error', 'binary_crossentropy'], default='mean_squared_error')
RELOAD_DATASET = False
RELOAD_TESTSET = False
RELOAD_MODEL = False
USE_OPTICAL_FLOW = False
BATCH_SIZE = 64
EPOCHS = 10

#Other Configs
CALCULATE_THRESHOLD = False
DISPAY_OUTPUT = True
LOAD_RESULT_FROM_CACHE = False
THRESHOLD_SCALING_FACTOR = 1.4
THRESHOLD_VALUE = 0.005138367473606623
