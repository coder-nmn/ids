"""
CNN-LSTM Hybrid Model for Intrusion Detection
Combines spatial (CNN) and temporal (LSTM) feature learning
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import pickle
import json
import os

class CNNLSTM_IDS:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None
        
    def build_model(self):
        """Build CNN-LSTM hybrid model"""
        print("Building CNN-LSTM model...")
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=self.input_shape),
            
            # CNN Block 1 - Spatial feature extraction
            layers.Conv1D(filters=128, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            # CNN Block 2
            layers.Conv1D(filters=64, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # LSTM Block 1 - Temporal pattern learning
            layers.LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.2),
            
            # LSTM Block 2
            layers.LSTM(64, dropout=0.3, recurrent_dropout=0.2),
            
            # Dense layers - Classification
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.4),
            
            # Output layer
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        self.model = model
        
        # Print model summary
        print("\nModel Architecture:")
        self.model.summary()
        
        return model
    
    def compile_model(self, learning_rate=0.001):
        """Compile model with optimizer and loss"""
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        print(f"Model compiled with learning_rate: {learning_rate}")
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=128):
        """Train the model"""
        print(f"\nTraining model...")
        print(f"Epochs: {epochs}, Batch size: {batch_size}")
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                'models/cnn_lstm_best.h5',
                save_best_only=True,
                monitor='val_accuracy',
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\nTraining complete!")
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        print("\nEvaluating model...")
        
        results = self.model.evaluate(X_test, y_test, verbose=1)
        
        # Get predictions for detailed metrics
        y_pred = self.model.predict(X_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        # Calculate metrics manually
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'loss': results[0],
            'accuracy': results[1],
            'precision': precision_score(y_test, y_pred_classes, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred_classes, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred_classes, average='weighted', zero_division=0)
        }
        
        print("\nTest Results:")
        print(f"Loss: {metrics['loss']:.4f}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        
        return metrics
    
    def save_model(self, filepath='models/cnn_lstm_final.h5'):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"\nModel saved to {filepath}")
        
        # Save training history
        if self.history:
            history_path = filepath.replace('.h5', '_history.json')
            with open(history_path, 'w') as f:
                json.dump(self.history.history, f)
            print(f"Training history saved to {history_path}")
    
    def load_model(self, filepath='models/cnn_lstm_final.h5'):
        """Load trained model"""
        self.model = tf.keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")
        return self.model
    
    def predict(self, X):
        """Make predictions"""
        predictions = self.model.predict(X)
        return predictions
    
    def predict_single(self, features):
        """Predict single sample (for API)"""
        # Reshape if needed
        if len(features.shape) == 2:
            features = np.expand_dims(features, axis=0)
        
        prediction = self.model.predict(features, verbose=0)
        pred_class = np.argmax(prediction[0])
        confidence = float(prediction[0][pred_class])
        
        return pred_class, confidence


def main():
    """Main training pipeline"""
    
    # Load preprocessed data
    print("Loading preprocessed data...")
    X_train = np.load('data/processed/X_train.npy')
    X_test = np.load('data/processed/X_test.npy')
    y_train = np.load('data/processed/y_train.npy')
    y_test = np.load('data/processed/y_test.npy')
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # Get number of classes
    num_classes = len(np.unique(y_train))
    print(f"Number of classes: {num_classes}")
    
    # Build model
    input_shape = (X_train.shape[1], X_train.shape[2])  # (sequence_length, features)
    ids_model = CNNLSTM_IDS(input_shape, num_classes)
    ids_model.build_model()
    ids_model.compile_model(learning_rate=0.001)
    
    # Train model
    history = ids_model.train(
        X_train, y_train,
        X_test, y_test,
        epochs=100,
        batch_size=128
    )
    
    # Evaluate model
    metrics = ids_model.evaluate(X_test, y_test)
    
    # Save model
    ids_model.save_model('models/cnn_lstm_final.h5')
    
    # Save metrics
    with open('models/cnn_lstm_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Final Accuracy: {metrics['accuracy']:.4f}")
    print(f"Final F1-Score: {metrics['f1_score']:.4f}")
    print("="*60)


if __name__ == "__main__":
    main()
