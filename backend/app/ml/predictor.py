import numpy as np
import pickle
from datetime import datetime
from typing import List, Dict, Any
from sklearn.ensemble import RandomForestClassifier
import structlog

logger = structlog.get_logger(__name__)


class SlotPredictor:
    def __init__(self, model_path: str = "vfsmax_predictor.onnx"):
        self.model_path = model_path
        self.model = None

    def train(self, history_data: List[Dict[str, Any]]):
        """Train a time-series model based on historical slot appearance."""
        # Features: hour, day_of_week, days_since_last_slot
        X = []
        y = []
        
        for record in history_data:
            dt = record["timestamp"]
            X.append([
                dt.hour,
                dt.weekday(),
                record["days_since_last_slot"]
            ])
            y.append(1 if record["slots_found"] > 0 else 0)

        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X, y)
        logger.info("Slot predictor model trained on history data", n_records=len(history_data))

    def predict(self, current_time: datetime, days_since_last_slot: int) -> float:
        """Predict probability of slots appearing in the next 30 minutes."""
        if not self.model:
            # Fallback to static probability baseline if model is not trained
            return 0.05
            
        features = np.array([[
            current_time.hour,
            current_time.weekday(),
            days_since_last_slot
        ]])
        
        # Get probability of class 1 (slot found)
        prob = self.model.predict_proba(features)[0][1]
        return float(prob)

    def save_model(self):
        """Save the trained model."""
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
            
    def load_model(self):
        """Load the trained model."""
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            logger.warning("No trained predictor model found at path", path=self.model_path)
