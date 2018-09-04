import keras
import pandas as pd
import numpy as np
from keras.layers import Dense, Input, Activation, LeakyReLU
from keras.models import Model, Sequential
from keras.optimizers import SGD, Adam


class NNAction:
    def __init__(self, input_dim=(100,), hidden_dim=64, output_dim=100, epsilon=0.2, bellman_value=0.95):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.q_model = self.build_q_model()
        self.target_q_model = self.build_q_model()
        self.epsilon = epsilon
        self.rl_memory = []
        self.bellman_value = bellman_value

    def build_q_model(self):
        model = Sequential([
            Dense(self.hidden_dim, input_shape=self.input_dim),
            LeakyReLU(),
            Dense(self.output_dim),
            # Dropout(self.epsilon),
            LeakyReLU(),
        ])
        model.compile(loss='mean_squared_error', optimizer=Adam(), metrics=['accuracy', 'mse'])
        return model

    @staticmethod
    def transform_state(state):
        return state.flatten().reshape(1, 100)

    def action(self, state):
        transformed_state = self.transform_state(state)
        if np.random.uniform(0, 1) > self.epsilon:
            action_prob = self.q_model.predict(transformed_state)[0]
            # print(transformed_state)
            # print(action_prob)
            action = np.argmax(action_prob)
        else:
            action = np.random.randint(self.output_dim)
        action_2d = (int((action - action % 10) / 10), action % 10)

        return action_2d

    def save_data(self, state_data, action_data, reward_data):
        for i in range(len(state_data)):
            if i == len(state_data) - 1:
                self.rl_memory.append((state_data[i], action_data[i], reward_data[i], None))
            else:
                self.rl_memory.append((state_data[i], action_data[i], reward_data[i],
                                       state_data[i + 1]))

    def prepare_train(self, batch):
        train_x = []
        train_y = []
        for i in batch:
            target_q = self.target_q_model.predict(self.transform_state(i[0]))[0]
            if i[3] is None:
                state_reward = i[2]
            else:
                state_reward = i[2] + self.bellman_value * self.target_q_model.predict(self.transform_state(i[3]))[
                    0].max()
            target_q[10 * i[1][0] + i[1][1]] = state_reward
            train_x.append(self.transform_state(i[0]))
            train_y.append(target_q.reshape((1, 100)))
        return np.concatenate(train_x), np.concatenate(train_y)

    def train(self):
        batch = self.rl_memory
        train_x, train_y = self.prepare_train(batch)
        self.q_model.fit(train_x, train_y)
        self.rl_memory = []

    def train_target_q(self):
        weights = self.target_q_model.get_weights()
        target_weights = self.q_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_q_model.set_weights(target_weights)


if __name__ == '__main__':
    nn = NNAction()
    for i in range(10):
        nn.save_data([np.random.rand(10, 10), np.random.rand(10, 10)],
                     [(np.random.randint(0, 10), np.random.randint(0, 10)),
                      (np.random.randint(0, 10), np.random.randint(0, 10))],
                     [np.random.randint(0, 2), np.random.randint(0, 2)])
    nn.train()
