from __future__ import annotations

import random
from typing import List

from models import Action, Agent, Bid, PublicState


class RandomAgent(Agent):
    def __init__(self, name:str="random"):
        super()
        self.name = name
    def decide(self, state_view: PublicState) -> Action:
        # Naive: prefer bids early, challenge sometimes
        def possible_bids() -> List[Bid]:
            total = sum(p.dice_remaining for p in state_view.players)
            cur = state_view.current_bid
            faces = state_view.faces
            out: List[Bid] = []
            for q in range(1, total + 1):
                for f in range(1, faces + 1):
                    b = Bid(q, f)
                    if cur is None or (b.quantity > cur.quantity) or (b.quantity == cur.quantity and b.face > cur.face):
                        out.append(b)
            return out

        bids = possible_bids()
        if bids and random.random() < 0.7:
            return Action(kind='bid', bid=random.choice(bids))
        # If there is a current bid, sometimes challenge/exact
        if state_view.current_bid is not None:
            if state_view.round_number % 2 == 0 and random.random() < 0.5 and state_view.wild_ones:
                return Action(kind='exact')
            return Action(kind='challenge')
        # Otherwise, must bid
        return Action(kind='bid', bid=bids[0] if bids else Bid(1, 1))
