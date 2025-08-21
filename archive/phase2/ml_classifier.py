import numpy as np
import tensorflow as tf
import requests
import json

# The 300-bit binary string from the Wow! signal analysis
WOW_BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

def generate_synthetic_data(num_samples, length):
    """
    Generates a synthetic dataset of celestial noise and human-generated signals.
    - Celestial noise is modeled as random binary data.
    - Human signals are modeled with simple patterns (e.g., repetition, simple sequences).
    """
    # Celestial noise (label 0)
    celestial_noise = np.random.randint(0, 2, size=(num_samples // 2, length))
    
    # Human-generated signals (label 1)
    human_signals = []
    for _ in range(num_samples // 2):
        pattern_type = np.random.choice(['repeat', 'sequence'])
        if pattern_type == 'repeat':
            pattern = np.random.randint(0, 2, size=(length // 10))
            signal = np.tile(pattern, 10)
        else: # sequence
            start = np.random.randint(0, 2)
            signal = np.array([(start + i) % 2 for i in range(length)])
        human_signals.append(signal)
    
    human_signals = np.array(human_signals)
    
    # Combine and shuffle the data
    X = np.vstack([celestial_noise, human_signals])
    y = np.array([0] * (num_samples // 2) + [1] * (num_samples // 2))
    
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    
    return X[indices], y[indices]

def create_and_train_model(X_train, y_train):
    """
    Creates and trains a simple neural network to classify signals.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(300,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)
    return model

def ask_ollama_about_ml_classification(wow_signal_data, prediction, confidence):
    """
    Sends the ML classification result to the Ollama LLM for interpretation.
    """
    print("\n--- Contacting Ollama instance for analysis of ML classification ---")
    
    classification = "likely artificial" if prediction > 0.5 else "likely natural (celestial noise)"
    
    prompt = f"""
    A machine learning model was trained to classify signals as either celestial noise (natural) or human-generated (artificial).
    The model was trained on a synthetic dataset where:
    - Celestial noise was modeled as random binary data.
    - Artificial signals were modeled with simple repeating patterns.

    The model was then used to classify the 300-bit Wow! signal.

    **Wow! Signal Binary Data:**
    ```
    {wow_signal_data}
    ```

    **Classification Result:**
    - The model classified the Wow! signal as **{classification}**.
    - The model's confidence in this prediction was **{confidence:.2%}**.

    **Request:**
    Based on this machine learning classification, please provide:
    1.  An interpretation of this result in the context of the Wow! signal investigation.
    2.  What are the limitations of this approach, given the synthetic nature of the training data?
    3.  What are the next steps to improve the reliability of this machine learning classification?
    """

    url = "http://127.0.0.1:11434/api/chat"
    data = {
        "model": "llama3.2:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_data = response.json()
        ollama_response = response_data['message']['content']
        print("\n--- Ollama's Response ---")
        print(ollama_response)
    except requests.exceptions.RequestException as e:
        print(f"\nError contacting Ollama instance: {e}")

if __name__ == "__main__":
    print("--- Machine Learning Classification of the Wow! Signal ---")

    # 1. Generate synthetic data for training
    print("\n[1] Generating synthetic training data...")
    X_train, y_train = generate_synthetic_data(num_samples=2000, length=300)
    print(f"Generated {len(X_train)} training samples.")

    # 2. Create and train the model
    print("\n[2] Creating and training the neural network...")
    model = create_and_train_model(X_train, y_train)

    # 3. Classify the Wow! signal
    print("\n[3] Classifying the Wow! signal...")
    wow_signal_numeric = np.array([int(bit) for bit in WOW_BINARY_STRING]).reshape(1, -1)
    prediction_prob = model.predict(wow_signal_numeric)[0][0]
    
    classification = "Artificial" if prediction_prob > 0.5 else "Natural"
    confidence = prediction_prob if classification == "Artificial" else 1 - prediction_prob
    
    print(f" -> Model Prediction: The Wow! signal is likely {classification}.")
    print(f" -> Confidence: {confidence:.2%}")

    # 4. Send the result to Ollama for interpretation
    ask_ollama_about_ml_classification(WOW_BINARY_STRING, prediction_prob, confidence)
