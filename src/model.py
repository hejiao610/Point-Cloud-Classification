import os
import numpy as np
import tensorflow as tf
from data_utils import get_filenames_and_class, generate_class_str_to_num_dict
from data_utils import get_points_and_class, read_off_file_into_nparray

class Model:
    def __init__(self, args):
        self.args = args
        self.train_list, self.test_list = get_filenames_and_class(args.Net10_data_dir)
        self.class_string_to_num = generate_class_str_to_num_dict(args.Net10_data_dir)
        self.point_net = self.build_point_net()

    def build_point_net(self):
        n_dims = 3

        initializer = tf.contrib.layers.xavier_initializer_conv2d()

        self.X = tf.placeholder(tf.float32, shape=(None, 1024, n_dims, 1), name='X')
        self.y = tf.placeholder(tf.int32, shape=(None))


        with tf.name_scope('point_net'):
            self.net = tf.layers.conv2d(inputs=self.X, filters=64, kernel_size=(1,3), padding='valid',
                                        activation=tf.nn.relu, kernel_initializer=initializer)
            self.net = tf.layers.conv2d(inputs=self.net, filters=64, kernel_size=(1,1), padding='valid',
                                        activation=tf.nn.relu, kernel_initializer=initializer)
            self.net = tf.layers.conv2d(inputs=self.net, filters=64, kernel_size=(1,1), padding='valid',
                                        activation=tf.nn.relu, kernel_initializer=initializer)
            self.net = tf.layers.conv2d(inputs=self.net, filters=128, kernel_size=(1, 1), padding='valid',
                                        activation=tf.nn.relu, kernel_initializer=initializer)
            self.net = tf.layers.conv2d(inputs=self.net, filters=1024, kernel_size=(1, 1), padding='valid',
                                        activation=tf.nn.relu, kernel_initializer=initializer)

            self.net = tf.layers.max_pooling2d(self.net, pool_size=[1024, 1],
                                               strides=(2,2), padding='valid')

            # self.net = tf.reshape(self.net, [-1])
            self.net = tf.layers.dense(self.net, 512, activation=tf.nn.relu,
                                       kernel_initializer=initializer)
            self.net = tf.layers.dense(self.net, 256, activation=tf.nn.relu,
                                       kernel_initializer=initializer)
            self.logits = tf.layers.dense(self.net, 10, activation=tf.nn.relu,
                                       kernel_initializer=initializer)

        with tf.name_scope('loss'):
            self.xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y, logits=self.logits)
            self.loss = tf.reduce_mean(self.xentropy)

        with tf.name_scope('train'):
            self.optimizer = tf.train.AdamOptimizer(learning_rate=self.args.learning_rate)
            self.training_op = self.optimizer.minimize(self.loss)

    def train(self):
        pass

    def test(self):
        pass

    def save(self):
        pass

    def load(self):
        pass