import redis

from dataset import IrisDataset
from algorithm import IrisDNN

EVENT_TRAIN = "BUILD_MODEL"

class IrisModelBuilder(object):
    def __init__(self, dataset_path, model_path, channels):
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.channels = channels

        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channels)

    def build_model(self):
        print("build iris model... ")

        # load dataset
        self.dataset = IrisDataset(self.dataset_path)

        # train model
        iris_dnn = IrisDNN(self.dataset, self.model_path)
        iris_dnn.train_model()
        iris_dnn.save_model()

    def build(self):
        self.build_model()

    def run(self):
        print("Listen build {} model command...".format(self.channels))

        for item in self.pubsub.listen():
            if item['data'] == EVENT_TRAIN:
                self.build()