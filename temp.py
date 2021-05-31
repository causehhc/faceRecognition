import tensorflow as tf
if __name__ == '__main__':
    print("GPU Available: ", tf.test.is_gpu_available())
    print(tf.test.gpu_device_name())
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    print(sess.run(hello))
