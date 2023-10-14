import random

suits = ["Heart", "Diamond", "Spade", "Clubs"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
value = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9,
         "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}

playing = True

class Cards():

    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def __str__(self):
        return self.ranks + " of " + self.suits

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Cards(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "the deck has " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = 0
        self.value_dict = value

    def addCard(self, card):
        self.cards.append(card)
        self.value += self.value_dict[card.ranks]
        if card.ranks == "Ace":
            self.ace += 1
        self.adjustForAces()

    def adjustForAces(self):
        while self.value > 21 and self.ace:
            self.value -= 10
            self.ace -= 1

class Chips():
    def __init__(self):
        self.total = 100
        self.bet = 0

    def winBet(self):
        self.total += 2 * self.bet
        self.bet = 0

    def loseBet(self):
        self.total -= self.bet
        self.bet = 0

def takeBet(chips):

    while True:
        try:
            print(f"\nYou have a total of {chips.total} chips")
            chips.bet = int(input("How much do u want to bet?: "))
            if chips.bet > chips.total:
                print("Sorry u don't have that many chips left!")
            else:
                chips.total -= chips.bet
                break
        except ValueError:
            print("A bet must be an integer!")

def player_hits(deck, hand):
    hand.addCard(deck.deal())
    hand.adjustForAces()

def dealer_hits(deck, hand):
    while hand.value < 17:
        player_hits(deck, hand)
    show_all(player_hand, dealer_hand)

def hit_or_stand(deck, hand):
    global playing

    while True:
        stay_or_hit = input("\n1. Draw Card\n2. Play\n- ")
        if stay_or_hit == '1':
            player_hits(deck, hand)
            show_some(player_hand, dealer_hand)
            if hand.value > 21:
                playing = True
                break
        elif stay_or_hit == '2':
            print("Player stays, dealer is playing!")
            playing = True
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

def show_some(player, dealer):
    print("\nDealer's hand:")
    print("**Hidden card**")
    print("-", dealer.cards[1])
    print("\nPlayer's hand:", *[(f"- {card}") for card in player.cards], sep="\n")

def show_all(player, dealer):
    print("\nDealer's hand : ", *dealer.cards, sep="\n")
    print("Dealer's hand value : ", dealer.value)
    print("\nPlayer's hand:", *[(f"- {card}") for card in player.cards], sep="\n")
    print("Player's hand value : ", player.value,"\n")

def player_busts(player, dealer, chips):
    print(f"The total values of you cards is {player_hand.value}")
    print("You bust!")
    print(f"You have {player_chips.total} left")
    global  playing
    playing = False

def player_wins(player, dealer, chips):
    print(f"Dealer has {dealer_hand.value} and you have {player_hand.value} ")
    print("You win!")
    chips.winBet()

def dealer_busts(player, dealer, chips):
    print(f"Dealers total values of theire cards is {dealer_hand.value}")
    print("Dealer busts!")
    chips.winBet()

def dealer_wins(player, dealer, chips):
    print(f"Dealer has {dealer_hand.value} and you have {player_hand.value} ")
    print("Dealer Wins")

def push(player, dealer, chips):
    print(f"Dealer has {dealer_hand.value} and you have {player_hand.value} ")
    print("You both have the same result!")
    print("It's a push!")

def reset_game():
    global playing, player_hand, dealer_hand
    global deck
    playing = True
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.addCard(deck.deal())
    player_hand.addCard(deck.deal())
    dealer_hand = Hand()
    dealer_hand.addCard(deck.deal())
    dealer_hand.addCard(deck.deal())
    takeBet(player_chips)

def play_again():
    global continue_playing , player_chips
    while True:
        continue_playing = input("Do you want to continue playing (y/n): ").lower()
        if continue_playing == 'y':
            break
        elif continue_playing == 'n':
            print(f'Congrats u won {player_chips.total}')
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

global deck
continue_playing = 'y'
player_chips = Chips()

#MAine game loop
while continue_playing == 'y':
    print("\n","*" * 5, "Welcome to blackjack", "*" * 5)
    print("-" * 3, "Get as close to 21 as u can without going over!", 3 * "-")


    takeBet(player_chips)
    reset_game()


    show_some(player_hand, dealer_hand)

    while playing:
        hit_or_stand(deck, player_hand)

        if player_hand.value > 21:
            playing = False
            player_busts(player_hand, dealer_hand, player_chips)
            if player_chips.total == 0:
                print("\nThanks for playing!")
                quit()
            else:
                play_again()
            break
        elif not playing:
            dealer_hits(deck, dealer_hand)
        elif player_hand.value <= 21:
            playing = False
            dealer_hits(deck, dealer_hand)
        if dealer_hand.value <= 21:
            if dealer_hand.value > player_hand.value:
                playing = False
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif player_hand.value > dealer_hand.value:
                playing = False
                player_wins(player_hand, dealer_hand, player_chips)
            elif player_hand.value == dealer_hand.value:
                playing = False
                push(player_hand, dealer_hand, player_chips)
        else:
            playing = False
            dealer_busts(player_hand, dealer_hand, player_chips)

        print("You have", player_chips.total, "chips left!")

        if continue_playing == 'n' or player_chips.total == 0:
            print("Thanks for playing!")
            break
        play_again()
