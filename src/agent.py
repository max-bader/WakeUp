import random
import pickle
from pathlib import Path
from typing import Any, Dict, List, Tuple

class QAgent:
    """
    Simple Q-learning agent for discrete (state, action) pairs
    """

    def __init__(
        self,
        actions: List[int],
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        qfile: Path = Path("qtable.pkl"),
    ) -> None:
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qfile = qfile
        self.q: Dict[Tuple[Any, Any], float] = {} # (state, action) -> Q


    def get_q(self, state: Any, action: Any) -> float:
        """
        Return Q-value for (state, action), default to 0.0
        """
        return self.q.get((state, action), 0.0)
    

    def choose_action(self, state: Any) -> Any:
        """
        Epsilon-greedy: with probability E pick random action,
        otherwise we pick action with highest Q for this state
        """
        # exploration: with probability epsilon, pick random action
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # greedy; build a mapping of action -> Q-value for this state
        q_vals = {a: self.get_q(state, a) for a in self.actions}

        # pick the action with the highest estimated Q-value
        return max(q_vals, key=q_vals.get)
    

    def learn(self, state, action, reward, next_state):
        """
        Perform a Q-learning update for the tuple (state, action):
            Q(s,a) ← Q(s,a) + α [ r + γ · maxₐ′ Q(s′, a′) − Q(s,a) ]
        where:
            • α is the learning rate
            • γ is the discount factor
            • r is the observed reward
            • maxₐ′ Q(s′,a′) is the estimated value of the best action in the next state
        """
        # retrieve current Q-value for (state, action)
        old = self.get_q(state, action)

        # estimate the best possible future reward from next_state by taking
        # the maximum Q-value over all available actions there
        future = max(self.get_q(next_state, a) for a in self.actions)

        # compute the TD-error: (reward + y * future) - old
        td_error = reward + self.gamma * future - old

        # update the Q-table entry for (state, action):
        # new_Q = old_Q + alpha * TD_error
        self.q[(state, action)] = old + self.alpha * td_error

    
    def save(self):
        with open(self.qfile, "wb") as f:
            pickle.dump(self.q, f)

    
    def load(self):
        if self.qfile.exists():
            with open(self.qfile, "rb") as f:
                self.q = pickle.load(f)