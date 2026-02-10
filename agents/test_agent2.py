from models import Action, Agent, Bid


class TestAgent2(Agent):
    def __init__(self, name:str="test2"):
        super()
        self.name = name
    def decide(self, state_view):
        current_bid = state_view.current_bid
        my_dice = state_view.my_dice
        faces = state_view.faces
        total = sum(p.dice_remaining for p in state_view.players)
        # Challenge only if bid is much higher than my dice
        if current_bid:
            face = int(current_bid.face)
            my_face_count = sum(1 for d in my_dice if d == face)
            if state_view.wild_ones and face != 1:
                my_face_count += sum(1 for d in my_dice if d == 1)
            if current_bid.quantity > my_face_count + (total // 2):
                return Action(kind='challenge')

        # Otherwise, bid up with the face I have most of
        face_counts = {f: my_dice.count(f) for f in range(1, faces + 1)}
        if state_view.wild_ones:
            for f in range(2, faces + 1):
                face_counts[f] += my_dice.count(1)
        best_face = max(face_counts, key=lambda f: face_counts[f])
        next_quantity = 1 if not current_bid else max(current_bid.quantity, 1) + 1
        return Action(kind='bid', bid=Bid(next_quantity, best_face))
