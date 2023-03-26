import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass

from tensorflow.image import resize
from tensorflow.keras.models import load_model


@dataclass
class AIModel:
    model_path: Path
    
    model = None

    def __post_init__(self):
        if self.model_path.exists():
            self.model = load_model(self.model_path)

    def get_model(self):
        if not self.model:
            raise Exception("Model not implemeted")
        return self.model
    def preprocessing(self, image_query):
        # Resize to 32*32
        x_pred = np.array([resize(image_query,[32,32])]).astype('float32')
        # Scale data
        x_input = x_pred / 255
        return x_input

    def predict(self, image_query):
        model = self.get_model()
        x_input = self.preprocessing(image_query)
        preds = model.predict(x_input)[0]
        # Convert One-hot vector to index
        idx = np.argmax(preds)
        labels= ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        return labels[idx], max(preds)