"""
Rețeaua neuronală Actor-Critic pentru control continuu cu PPO.
Include rețeaua actor (distribuție gaussiană diagonală) și rețeaua critic (valoarea stării V).
"""

import numpy as np
import torch
import torch.nn as nn
from torch.distributions.normal import Normal


def layer_init(layer: nn.Linear, std: float = np.sqrt(2), bias_const: float = 0.0) -> nn.Linear:
    """Inițializează ortogonal ponderile unui strat liniar și setează bias-ul constant."""
    nn.init.orthogonal_(layer.weight, std)
    nn.init.constant_(layer.bias, bias_const)
    return layer


class ActorCritic(nn.Module):
    """Arhitectură Actor-Critic pentru spații de acțiuni continue."""

    def __init__(self, obs_dim: int, act_dim: int, hidden_dim: int = 64):
        super().__init__()
        self.obs_dim = obs_dim
        self.act_dim = act_dim

        # Rețeaua critic estimează valoarea stării V(s)
        self.critic = nn.Sequential(
            layer_init(nn.Linear(obs_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, 1), std=1.0),
        )

        # Rețeaua actor prezice media acțiunilor mu(s)
        self.actor_mean = nn.Sequential(
            layer_init(nn.Linear(obs_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, hidden_dim)),
            nn.Tanh(),
            layer_init(nn.Linear(hidden_dim, act_dim), std=0.01),
        )

        # Logaritmul deviației standard (log_std), parametru învățabil independent de stare
        self.actor_logstd = nn.Parameter(torch.zeros(1, act_dim))

    def get_value(self, x: torch.Tensor) -> torch.Tensor:
        """Calculează valoarea estimată a stării V(s)."""
        return self.critic(x)

    def get_action_and_value(
        self, x: torch.Tensor, action: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Produce acțiunea eșantionată, log-probabilitatea, entropia și valoarea stării.
        Dacă este furnizată o acțiune existentă, calculează log-probabilitatea și entropia acesteia.
        """
        action_mean = self.actor_mean(x)
        action_logstd = self.actor_logstd.expand_as(action_mean)
        action_std = torch.exp(action_logstd)
        probs = Normal(action_mean, action_std)

        if action is None:
            action = probs.sample()

        # Pentru distribuții multivariate diagonale, log-probabilitatea este suma pe dimensiuni
        log_prob = probs.log_prob(action).sum(axis=-1)
        entropy = probs.entropy().sum(axis=-1)
        value = self.critic(x)

        return action, log_prob, entropy, value

    def predict(self, x: torch.Tensor, deterministic: bool = True) -> torch.Tensor:
        """Produce o acțiune pentru evaluare (implicit deterministă, prin media distribuției)."""
        action_mean = self.actor_mean(x)
        if deterministic:
            return action_mean
        action_std = torch.exp(self.actor_logstd.expand_as(action_mean))
        return Normal(action_mean, action_std).sample()
