import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
value = {"ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "jack": 10, "queen": 10, "king": 10}


root = tk.Tk()
root.title("Blackjack Game")
root.geometry("800x600")

background_image = Image.open("table.png")
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)


canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")


card_images = {}
for suit in suits:
    for rank in ranks:
        card_name = f"{rank}_of_{suit}.png"
        img = Image.open(f"images/{card_name}")
        img = img.resize((100, 150), Image.Resampling.LANCZOS)
        card_images[f"{rank} of {suit}"] = ImageTk.PhotoImage(img)


question_mark_img = Image.open("question_mark.png")
question_mark_img = question_mark_img.resize((100, 150), Image.Resampling.LANCZOS)
question_mark_photo = ImageTk.PhotoImage(question_mark_img)


class Cards:
    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def __str__(self):
        return self.ranks + " of " + self.suits


class Deck:
    def __init__(self):
        self.deck = [Cards(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = 0
        self.value_dict = value

    def addCard(self, card):
        self.cards.append(card)
        self.value += self.value_dict[card.ranks]
        if card.ranks == "ace":
            self.ace += 1
        self.adjustForAces()

    def adjustForAces(self):
        while self.value > 21 and self.ace:
            self.value -= 10
            self.ace -= 1


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def winBet(self):
        self.total += 2 * self.bet
        self.bet = 0

    def loseBet(self):
        self.total -= self.bet
        self.bet = 0


dealer_label = tk.Label(root, text="", font=("Arial", 14), bg="white", fg="white")
canvas.create_window(400, 50, window=dealer_label)

player_label = tk.Label(root, text="", font=("Arial", 14), bg="white", fg="white")
canvas.create_window(400, 500, window=player_label)

chips_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="white", fg="black")
canvas.create_window(400, 50, window=chips_label)

dealer_card_frame = tk.Frame(root)
canvas.create_window(400, 150, window=dealer_card_frame)

player_card_frame = tk.Frame(root)
canvas.create_window(400, 400, window=player_card_frame)

button_frame = tk.Frame(root, bg="cyan")
canvas.create_window(400, 550, window=button_frame)

global hit_button, stand_button
hit_button = tk.Button(button_frame, text="Hit", command=lambda: None,  fg="black", font=("Arial", 14, "bold"))
hit_button.pack(side=tk.LEFT, padx=0, pady=0, fill=tk.BOTH, expand=True)

stand_button = tk.Button(button_frame, text="Stand", command=lambda: None,  fg="black", font=("Arial", 14, "bold"))
stand_button.pack(side=tk.LEFT, padx=0, pady=0, fill=tk.BOTH, expand=True)

hit_button.config(state=tk.DISABLED)
stand_button.config(state=tk.DISABLED)

top_right_frame = tk.Frame(root, bg="white")
canvas.create_window(750, 80, window=top_right_frame)

def show_some(player, dealer):
    for widget in dealer_card_frame.winfo_children():
        widget.destroy()
    for widget in player_card_frame.winfo_children():
        widget.destroy()

    dealer_first_card = tk.Label(dealer_card_frame, image=question_mark_photo)
    dealer_first_card.pack(side=tk.LEFT)
    dealer_second_card = tk.Label(dealer_card_frame, image=card_images[str(dealer.cards[1])])
    dealer_second_card.pack(side=tk.LEFT)

    for card in player.cards:
        card_img = tk.Label(player_card_frame, image=card_images[str(card)])
        card_img.pack(side=tk.LEFT)

    chips_label.config(text=f"Chips: {player_chips.total}")

def show_all(player, dealer):

    for widget in dealer_card_frame.winfo_children():
        widget.destroy()
    for widget in player_card_frame.winfo_children():
        widget.destroy()

    # Dealer's hand
    for card in dealer.cards:
        card_img = tk.Label(dealer_card_frame, image=card_images[str(card)])
        card_img.pack(side=tk.LEFT)


    for card in player.cards:
        card_img = tk.Label(player_card_frame, image=card_images[str(card)])
        card_img.pack(side=tk.LEFT)

    chips_label.config(text=f"Chips: {player_chips.total}")

def take_bet_on_window():

    for widget in top_right_frame.winfo_children():
        widget.destroy()

    bet_label = tk.Label(top_right_frame, text="Enter your bet", font=("Arial", 10, "bold"), bg="white", fg="black")
    bet_label.pack(pady=5)
    bet_label = tk.Label(top_right_frame, text="to start playing:", font=("Arial", 10, "bold"), bg="white", fg="black")
    bet_label.pack(pady=5)
    def submit_bet():
        try:
            bet = int(bet_entry.get())
            if bet > player_chips.total:
                messagebox.showinfo("Error", "Sorry, you don't have enough chips!")
            elif bet <= 0:
                messagebox.showinfo("Error", "Please enter a positive bet!")
            else:
                player_chips.bet = bet
                player_chips.total -= bet
                chips_label.config(text=f"Chips: {player_chips.total}")
                bet_entry.config(state=tk.DISABLED)
                submit_bet_button.config(state=tk.DISABLED)
                hit_button.config(state=tk.NORMAL)  # Enable 'Hit' and 'Stand' buttons after valid bet
                stand_button.config(state=tk.NORMAL)
                hit_or_stand(deck, player_hand)
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid number for the bet.")

    global bet_entry
    bet_entry = tk.Entry(top_right_frame, bg="white", highlightbackground="black", highlightthickness=4)
    bet_entry.pack(pady=10, fill=tk.BOTH)

    global submit_bet_button
    submit_bet_button = tk.Button(top_right_frame, text="Submit Bet", command=submit_bet)
    submit_bet_button.pack(pady=3, fill=tk.X, expand=True)



def hit_or_stand(deck, hand):

    def hit():
        player_hits(deck, hand)
        show_some(player_hand, dealer_hand)
        if hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

    def stand():
        dealer_hits(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    hit_button.config(command=hit)
    stand_button.config(command=stand)


def player_hits(deck, hand):
    hand.addCard(deck.deal())
    show_some(player_hand, dealer_hand)


def dealer_hits(deck, hand):
    while hand.value < 17:
        hand.addCard(deck.deal())
    show_all(player_hand, dealer_hand)


def player_busts(player, dealer, chips):
    messagebox.showinfo("Game Over", "You bust!")
    reset_game()


def player_wins(player, dealer, chips):
    messagebox.showinfo("Game Over", "You win!")
    chips.winBet()
    reset_game()


def dealer_busts(player, dealer, chips):
    messagebox.showinfo("Game Over", "Dealer busts, you win!")
    chips.winBet()
    reset_game()


def dealer_wins(player, dealer, chips):
    messagebox.showinfo("Game Over", "Dealer wins!")
    reset_game()


def push(player, dealer):
    messagebox.showinfo("Game Over", "It's a push!")
    reset_game()

def show_result(message):
    messagebox.showinfo("Game Over", message)
    if player_chips.total > 0:
        reset_game()
    else:
        end_game()




def reset_game():
    global deck, player_hand, dealer_hand
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)

    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.addCard(deck.deal())
    player_hand.addCard(deck.deal())
    dealer_hand = Hand()
    dealer_hand.addCard(deck.deal())
    dealer_hand.addCard(deck.deal())

    show_some(player_hand, dealer_hand)
    take_bet_on_window()
    end_game_button = tk.Button(top_right_frame, text="End Game", command=end_game)
    end_game_button.pack(fill= tk.X, expand=True)

    if player_chips.total == 0:
        messagebox.showinfo("Defeat!","You dont have any more chips left")
        quit()




def end_game():
    chips_after_game = player_chips.total - 100
    if chips_after_game > 0:
        messagebox.showinfo("Game Over", f"You have won {chips_after_game} chips!")
        root.after(100, root.quit)
    else:
        chips_after_game = chips_after_game * (-1)
        messagebox.showinfo("Game Over", f"You have lost {chips_after_game} chips!")




player_chips = Chips()
reset_game()
root.mainloop()
