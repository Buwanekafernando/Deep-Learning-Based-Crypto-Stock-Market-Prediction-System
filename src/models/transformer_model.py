import tensorflow as tf
from tensorflow.keras import layers


def build_transformer_model(seq_len, n_features, d_model=64, num_heads=4):

    inputs = layers.Input(shape=(seq_len, n_features))

    # Project features
    x = layers.Dense(d_model)(inputs)

    # Multi-Head Attention
    attention_output = layers.MultiHeadAttention(
        num_heads=num_heads,
        key_dim=d_model
    )(x, x)

    x = layers.Add()([x, attention_output])
    x = layers.LayerNormalization()(x)

    # Feed Forward
    ff = layers.Dense(128, activation="relu")(x)
    ff = layers.Dense(d_model)(ff)

    x = layers.Add()([x, ff])
    x = layers.LayerNormalization()(x)

    x = layers.GlobalAveragePooling1D()(x)

    outputs = layers.Dense(1)(x)

    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["mae"]
    )

    return model