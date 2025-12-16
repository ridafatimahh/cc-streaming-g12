import tensorflow as tf
import numpy as np
import os

# 1. Generate synthetic training data
# We match the producer: 4 features, normally distributed
X_train = np.random.normal(loc=0.0, scale=1.0, size=(1000, 4))
# Generate fake labels (0 or 1) based on a simple rule
y_train = (np.sum(X_train, axis=1) > 0).astype(int)

# 2. Define a simple Keras model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid') # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. Train the model
print("Training model...")
model.fit(X_train, y_train, epochs=5)

# 4. Save the model for TensorFlow Serving
# The path must be: data/model/my_model/1/
# (TF Serving requires a version number, here '1')
export_path = os.path.join("data", "model", "my_model", "1")

print(f"Saving model to {export_path}...")
tf.saved_model.save(model, export_path)
print("Model saved successfully!")
