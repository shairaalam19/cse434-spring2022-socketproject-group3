from decimal import InvalidContext


def duplicates(cards):
    showCards = []
    for card in cards: 
        if card not in showCards:
            showCards.append(card)
        else: 
            index = showCards.index(card)
            showCards.pop(index)
    return showCards

cards = [1, 1, 2, 1, 2, 3, 4]
print(duplicates(cards))