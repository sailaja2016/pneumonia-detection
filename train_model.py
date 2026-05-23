"""
train_model.py
──────────────
Trains a CNN on the Kaggle Chest X-Ray dataset and saves the model
to model/pneumonia_model.h5

Dataset: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

Usage:
    python train_model.py

Requirements:
    pip install tensorflow pillow numpy
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ── Paths ──────────────────────────────────────────────────────────────
DATASET_DIR = os.path.join(os.path.dirname(__file__), 'chest_xray')
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'model', 'pneumonia_model.h5')

TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR   = os.path.join(DATASET_DIR, 'val')
TEST_DIR  = os.path.join(DATASET_DIR, 'test')

# ── Hyperparameters ────────────────────────────────────────────────────
IMG_SIZE    = (150, 150)
BATCH_SIZE  = 32
EPOCHS      = 20


def build_model():
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        # Block 2
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        # Block 3
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        # Block 4
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        # Classifier Head
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Binary: Normal vs Pneumonia
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model


def main():
    # ── Data Generators ──────────────────────────────────────────────
    # Training: augment to reduce overfitting
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Validation & Test: only normalize
    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    val_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    test_gen = val_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )

    # ── Build & Train ──────────────────────────────────────────────────
    model = build_model()
    model.summary()

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    callbacks = [
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, monitor='val_accuracy', verbose=1),
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    ]

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks
    )

    # ── Evaluate on Test Set ───────────────────────────────────────────
    print("\n── Test Set Evaluation ──")
    loss, accuracy = model.evaluate(test_gen)
    print(f"Test Loss:     {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")


if __name__ == '__main__':
    main()
