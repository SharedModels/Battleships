import keras
import pandas as pd
import numpy as np
from keras.layers import Dense, Input, Activation, LeakyReLU, Dropout, Conv2D, Flatten
from keras.models import Model, Sequential
from keras.optimizers import SGD, Adam


class NNAction:
    def __init__(self, input_dim=(10, 10, 1), hidden_dim=64, output_dim=100, epsilon=1, bellman_value=0.95,
                 buffer_size=40000):
        """
        class to predict actions for battleships game, using reinforcement learning.
        :param input_dim: tuple
         Input shape for NN
        :param hidden_dim: integer
         hidden layer size (not used for cnn as too complex)
        :param output_dim: integer
        output size for NN
        :param epsilon: float
        Value for e greedy policy, decays by 0.99 every training session
        :param bellman_value: float
        value to use in bellman equation
        :param buffer_size: integer
        size of rl buffer
        """
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.q_model = self.build_cnn_model()
        self.target_q_model = self.build_cnn_model()
        self.epsilon = epsilon
        self.rl_memory = []
        self.bellman_value = bellman_value
        self.buffer_size = buffer_size

    def build_q_model(self):
        """
        First attempt at building a flat model for battleships, does not work well.
        :return: keras model
        """
        model = Sequential()
        model.add(Dense(self.hidden_dim, input_shape=self.input_dim))
        model.add(Activation('relu'))
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dense(self.output_dim))
        model.add(Activation('relu'))

        # [
        #     Dense(self.hidden_dim, input_shape=self.input_dim),
        #     LeakyReLU(),
        #     Dense(self.output_dim),
        #     # Dropout(0.5),
        #     LeakyReLU(),
        # ])
        model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy', 'mse'])
        return model

    def build_cnn_model(self):
        """
        CNN for battleships, seems to work a lot better than flat version
        :return: keras model
        """
        model = Sequential()
        model.add(Conv2D(32, input_shape=(10, 10, 1), kernel_size=(5, 5)))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3), strides=(3, 3)))
        model.add(Activation('relu'))
        # model.add(Conv2D(64, (3, 3), strides=(1, 1)))
        # model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(self.hidden_dim))
        model.add(Activation('relu'))
        model.add(Dense(self.output_dim))
        model.add(Activation('linear'))
        model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy', 'mse'])
        return model

    @staticmethod
    def transform_state(state):
        """
        Transform state into shape needed for flattened model
        :param state: numpy array shape (10, 10)
        :return: numpy array shape (1, 100
        """
        return state.flatten().reshape(1, 100)

    @staticmethod
    def transform_state_cnn(state):
        """
        Transform state into shape for cnn, add in a 1d channel. This might just be because used COnv2D where not nesc.
        :param state: numpy array shape (10, 10)
        :return: numpy array shape (1, 10, 10, 1)
        """
        return state.reshape(1, 10, 10, 1)

    def action(self, state):
        """
        Perform an action in battleships. Uses e-greedy policy where there is self.epsilon chance to just use a random
        action.
        :param state: numpy array shape (10, 10)
        :return: integer location of attack
        """
        transformed_state = self.transform_state_cnn(state)
        if np.random.uniform(0, 1) > self.epsilon:
            action_prob = self.q_model.predict(transformed_state)[0]
            # Anything that is non-zero in the state is an invalid move, this makes it so invalid moves cant be used
            action_prob[state.flatten() != 0] = -100
            action = np.argmax(action_prob)
        else:
            action = np.random.randint(self.output_dim)
        # Transform a 1d action into 2d for the game
        action_2d = (int((action - action % 10) / 10), action % 10)

        return action_2d

    def save_data(self, state_data, action_data, reward_data):
        """
        Save incoming data into the class rl_memory. Unless this is the last state, keep the next state in the tuple for
        calculating q values in the future. All lists must be the same length
        :param state_data: list of arrays
        :param action_data: list of tuples
        :param reward_data: list of integers
        """
        for i in range(len(state_data)):
            if i == len(state_data) - 1:
                self.rl_memory.append((state_data[i], action_data[i], reward_data[i], None))
            else:
                self.rl_memory.append((state_data[i], action_data[i], reward_data[i],
                                       state_data[i + 1]))

    def prepare_train(self, batch):
        """
        Prepare the training data. Predict reward for all other actions that werent taken, add on reward for the next
        step for the action that was taken.
        :param batch: list of tuples
        :return: train_x numpy array of states, train_y numpy array of rewards
        """
        train_x = []
        train_y = []
        for i in batch:
            # print(self.transform_state_cnn(i[0]))
            target_q = self.target_q_model.predict(self.transform_state_cnn(i[0]))[0]
            if i[3] is None:
                state_reward = i[2]
            else:
                state_reward = i[2] + self.bellman_value * self.target_q_model.predict(self.transform_state_cnn(i[3]))[
                    0].max()

            target_q[10 * i[1][0] + i[1][1]] = state_reward
            # target_q[i[0].flatten() != 0] = 0
            train_x.append(self.transform_state_cnn(i[0]))
            train_y.append(target_q.reshape((1, 100)))
        return np.concatenate(train_x), np.concatenate(train_y)

    def pick_rl(self):
        """
        Pick random batch of states for training
        :return: list
        """
        idx = np.random.choice(range(len(self.rl_memory)), 128, replace=True)
        return [self.rl_memory[i] for i in idx]

    def train(self):
        """
        Train the rl model, also reduces the size of self.epsilon
        """
        batch = self.pick_rl()

        train_x, train_y = self.prepare_train(batch)
        self.q_model.fit(train_x, train_y)
        self.rl_memory = self.rl_memory[-self.buffer_size:]
        self.epsilon *= 0.9

    def train_target_q(self):
        """
        Update the target q model weights.
        """
        weights = self.q_model.get_weights()
        target_weights = self.target_q_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_q_model.set_weights(target_weights)

    def save(self):
        """
        Save the keras model
        """
        self.q_model.save('q_model.h5')


if __name__ == '__main__':
    nn = NNAction()
    for i in range(10):
        nn.save_data([np.random.rand(10, 10), np.random.rand(10, 10)],
                     [(np.random.randint(0, 10), np.random.randint(0, 10)),
                      (np.random.randint(0, 10), np.random.randint(0, 10))],
                     [np.random.randint(0, 2), np.random.randint(0, 2)])
    nn.train()
