import gym
from gym import spaces
from gym.utils import seeding
import numpy as np


class OXGameEnv(gym.Env):
    def __init__(self):
        self.board = np.zeros((3, 3))  # 3x3の盤面を作成
        self.current_player = 1  # 最初のプレイヤーは1番
        self.action_space = spaces.Discrete(9)  # 行動空間は0から8までの整数
        self.observation_space = spaces.Box(low=-1, high=1, shape=(3, 3), dtype=np.int32)  # 盤面の状態を表す
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1
        return self.board

    def step(self, action):
        row = action // 3
        col = action % 3

        if self.board[row][col] != 0:
            return self.board, -10, True, {}  # すでに占有された場所には置けない

        self.board[row][col] = self.current_player

        if self._is_winner(self.current_player):
            reward = 10
            done = True
        elif self._is_board_full():
            reward = 0
            done = True
        else:
            reward = 0
            done = False

        self.current_player = -self.current_player  # プレイヤーを交代する

        return self.board, reward, done, {}

    def _is_winner(self, player):
        # 行で勝利したかどうか
        for i in range(3):
            if all(self.board[i] == player):
                return True
        # 列で勝利したかどうか
        for i in range(3):
            if all(self.board[:, i] == player):
                return True
        # 対角線で勝利したかどうか
        if all(self.board.diagonal() == player) or all(np.fliplr(self.board).diagonal() == player):
            return True
        return False

    def _is_board_full(self):
        return not (self.board == 0).any()

    def render(self, mode='human'):
        for row in self.board:
            print('|', end='')
            for col in row:
                if col == 1:
                    print('X', end='|')
                elif col == -1:
                    print('O', end='|')
                else:
                    print('_', end='|')
            print('')
        print('')


class RandomAgentV1:
    def __init__(self, env):
        self.action_space = env.action_space

    def choose_action(self):
        return self.action_space.sample()  # 行動空間からランダムに行動を選択する


class RandomAgentV2:
    def __init__(self, env):
        self.env = env

    def choose_action(self):
        valid_actions = np.where(self.env.board == 0)[0]  # 空の位置を取得
        return np.random.choice(valid_actions)  # 空の位置からランダムに行動を選択


def vs_player(env):
    _ = env.reset()

    done = False
    while not done:
        env.render()
        print("It is the turn of {}.".format('X' if env.current_player == 1 else 'O'))
        action = int(input("Enter your move (0-8): "))
        observation, reward, done, info = env.step(action)
        print(f"Reward: {reward}")
        if done:
            if reward == 10:
                print("You win!")
            elif reward == 0:
                print("It's a draw!")


def vs_random_agent(env):
    agent = RandomAgentV2(env)

    _ = env.reset()
    done = False
    while not done:
        env.render()
        print("It is the turn of {}.".format('X' if env.current_player == 1 else 'O'))
        if env.current_player == 1 :
            action = int(input("Enter your move (0-8): "))
        else:
            action = agent.choose_action()
        obs, reward, done, info = env.step(action)
        print(f"Agent's action: {action}")
        if done:
            if reward == 10:
                print("You win!")
            elif reward == 0:
                print("It's a draw!")
        env.render()


def main():
    env = OXGameEnv()
    _ = env.reset()

    play_mode = int(input("Enter your play mode (0 or 1)\n 0: 2 Player\n 1: VS Random agent\ninput : "))
    if play_mode == 0:
        vs_player(env)
    elif play_mode == 1:
        vs_random_agent(env)


if __name__ == '__main__':
    main()