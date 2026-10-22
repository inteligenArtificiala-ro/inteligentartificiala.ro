"""
Buffer pentru stocarea traiectoriilor (rollout buffer) și calculul GAE.
"""

from typing import Generator
import numpy as np
import torch


class RolloutBuffer:
    """Stochează tranzițiile generate de medii paralele și calculează avantajele GAE."""

    def __init__(
        self,
        num_steps: int,
        num_envs: int,
        obs_dim: int,
        act_dim: int,
        device: torch.device,
    ):
        self.num_steps = num_steps
        self.num_envs = num_envs
        self.device = device

        self.obs = torch.zeros((num_steps, num_envs, obs_dim), device=device)
        self.actions = torch.zeros((num_steps, num_envs, act_dim), device=device)
        self.logprobs = torch.zeros((num_steps, num_envs), device=device)
        self.rewards = torch.zeros((num_steps, num_envs), device=device)
        self.dones = torch.zeros((num_steps, num_envs), device=device)
        self.values = torch.zeros((num_steps, num_envs), device=device)

        self.advantages = torch.zeros((num_steps, num_envs), device=device)
        self.returns = torch.zeros((num_steps, num_envs), device=device)

    def insert(
        self,
        step: int,
        obs: torch.Tensor,
        action: torch.Tensor,
        logprob: torch.Tensor,
        reward: torch.Tensor,
        done: torch.Tensor,
        value: torch.Tensor,
    ) -> None:
        """Adaugă tranziția de la pasul curent în buffer."""
        self.obs[step] = obs
        self.actions[step] = action
        self.logprobs[step] = logprob
        self.rewards[step] = reward
        self.dones[step] = done
        self.values[step] = value.flatten()

    def compute_gae(
        self,
        next_value: torch.Tensor,
        next_done: torch.Tensor,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
    ) -> None:
        """
        Calculează estimarea generalizată a avantajului (GAE) și recompensele cumulate țintă.
        Algoritmul parcurge pașii în ordine inversă: de la t = T-1 până la 0.
        """
        lastgaelam = 0.0
        for t in reversed(range(self.num_steps)):
            if t == self.num_steps - 1:
                nextnonterminal = 1.0 - next_done.float()
                nextvalues = next_value.flatten()
            else:
                nextnonterminal = 1.0 - self.dones[t + 1]
                nextvalues = self.values[t + 1]

            delta = self.rewards[t] + gamma * nextvalues * nextnonterminal - self.values[t]
            lastgaelam = delta + gamma * gae_lambda * nextnonterminal * lastgaelam
            self.advantages[t] = lastgaelam

        self.returns = self.advantages + self.values

    def get_generator(
        self, minibatch_size: int
    ) -> Generator[tuple[torch.Tensor, ...], None, None]:
        """
        Aplatizează datele adunate din toate mediile și generează mini-loturi amestecate aleator.
        """
        batch_size = self.num_steps * self.num_envs
        b_obs = self.obs.reshape((-1, self.obs.shape[-1]))
        b_actions = self.actions.reshape((-1, self.actions.shape[-1]))
        b_logprobs = self.logprobs.reshape(-1)
        b_advantages = self.advantages.reshape(-1)
        b_returns = self.returns.reshape(-1)
        b_values = self.values.reshape(-1)

        indices = np.random.permutation(batch_size)
        for start in range(0, batch_size, minibatch_size):
            end = start + minibatch_size
            mb_inds = indices[start:end]
            yield (
                b_obs[mb_inds],
                b_actions[mb_inds],
                b_logprobs[mb_inds],
                b_advantages[mb_inds],
                b_returns[mb_inds],
                b_values[mb_inds],
            )
