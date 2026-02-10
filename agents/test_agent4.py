import random

from models import Action, Agent, Bid


class TestAgent4(Agent):
    def __init__(self, name:str="test4"):
        super()
        self.name = name
    def decide(self, state_view):
        current_bid = state_view.current_bid
        my_dice = state_view.my_dice
        faces = state_view.faces
        total = sum(p.dice_remaining for p in state_view.players)
        # 20% chance to call exact if plausible
        if current_bid and random.random() < 0.2:
            face = int(current_bid.face)
            my_face_count = sum(1 for d in my_dice if d == face)
            if state_view.wild_ones and face != 1:
                my_face_count += sum(1 for d in my_dice if d == 1)
            if abs(my_face_count - current_bid.quantity) <= 1:
                return Action(kind='exact')
        # 30% chance to challenge if bid is high
        if current_bid and random.random() < 0.3:
            if current_bid.quantity > (total // 2) + 1:
                return Action(kind='challenge')
        # Otherwise, bid up with a random face I have or random legal bid
        possible_bids = []
        for q in range(1, total + 1):
            for f in range(1, faces + 1):
                if f in my_dice:
                    possible_bids.append(Bid(q, f))
        if not possible_bids:
            possible_bids = [Bid(1, f) for f in range(1, faces + 1)]
        return Action(kind='bid', bid=random.choice(possible_bids))
