import random

from models import Action, Agent, Bid


class TestAgent3(Agent):
    def __init__(self, name:str="test3"):
        super()
        self.name = name
    def decide(self, state_view):
        current_bid = state_view.current_bid
        my_dice = state_view.my_dice
        faces = state_view.faces
        total = sum(p.dice_remaining for p in state_view.players)
        # If current bid matches my dice, call exact
        if current_bid:
            face = int(current_bid.face)
            my_face_count = sum(1 for d in my_dice if d == face)
            if state_view.wild_ones and face != 1:
                my_face_count += sum(1 for d in my_dice if d == 1)
            if my_face_count == current_bid.quantity:
                return Action(kind='exact')
            # If bid is very risky, challenge
            if current_bid.quantity > my_face_count + (total // 2):
                return Action(kind='challenge')

        # Otherwise, bid up with a random face I have
        faces_i_have = [d for d in set(my_dice)]
        if not faces_i_have:
            faces_i_have = list(range(1, faces + 1))
        next_quantity = 1 if not current_bid else max(current_bid.quantity, 1) + 1
        return Action(kind='bid', bid=Bid(next_quantity, random.choice(faces_i_have)))
