import pytest
from src.agent import QAgent

def test_get_and_learn():
    agent = QAgent(actions=[0], alpha=0.5, gamma=0, epsilon=0)
    assert agent.get_q("s","a") == 0.0
    
    agent.learn("s", "a", reward=4, next_state="s2")
    assert agent.get_q("s","a") == pytest.approx(2.0) # 0 + 0.5 * (4 + 0 - 0)


def test_choose_greedy():
    agent = QAgent(actions=[1,2], epsilon=0)
    
    # manually seed Q
    agent.q = {("st", 1): 5.0, ("st", 2): 3.0}
    assert agent.choose_action("st") == 1