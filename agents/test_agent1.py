from models import Action, Agent, Bid
import random

class TestAgent1(Agent):
    def __init__(self, name:str="test1"):
        super()
        self.name=name
    def decide(self, state_view):
        """
        A robust agent that:
        - Challenges if the current bid is much higher than its own dice count for that face.
        - Otherwise, bids on a face it has, preferring faces it has the most of.
        """
        current_bid = state_view.current_bid
        my_dice = state_view.my_dice
        faces = state_view.faces
        total = sum(p.dice_remaining for p in state_view.players)

        # Count dice for each face (including wild ones)
        face_counts = {f: my_dice.count(f) for f in range(1, faces + 1)}
        if state_view.wild_ones:
            for f in range(2, faces + 1):
                face_counts[f] += my_dice.count(1)

        # If there is a current bid, challenge if it's much higher than my dice
        if current_bid:
            face = int(current_bid.face)
            my_face_count = face_counts[face]
            # Challenge if the bid is more than what I have + half the total dice
            if current_bid.quantity > my_face_count + (total // 2):
                return Action(kind='challenge')

        # Otherwise, bid up with the face I have most of
        best_face = max(face_counts, key=lambda f: face_counts[f])
        next_quantity = 1 if not current_bid else max(current_bid.quantity, 1) + 1
        return Action(kind='bid', bid=Bid(next_quantity, best_face))
