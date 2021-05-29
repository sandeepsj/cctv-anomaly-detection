
DATASET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Train"
TESTSET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test"
#TESTSET_PATH = "/home/sandeepsj/Desktop"
TARGET_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test/UCSDped1.m"
SINGLE_TEST_PATH = "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test/Test001"
TESTSET_STRUCTURE = "dict" # ["dict", "array_seq"]
RELOAD_DATASET = False
RELOAD_TESTSET = False
RELOAD_MODEL = False
USE_OPTICAL_FLOW = False
MODEL_NAME = "convolutional_autoencoder" # ['autoencoder', 'deep_autoencoder', 'convolutional_autoencoder']
CACHE_PATH = "cache"
MODEL_PATH = "/home/sandeepsj/cctv-anomaly-detection/models"
BATCH_SIZE = 64
EPOCHS = 10
OPTIMIZER = "adam" # ['adam','sgd','adagrad']
LOSS = "mean_squared_error" # ['mean_squared_error', 'binary_crossentropy'], default='mean_squared_error')
TEST_SAMPLES = 50
RESULT_PATH = "/home/sandeepsj/cctv-anomaly-detection/results"
LOAD_RESULT_FROM_CACHE = False
