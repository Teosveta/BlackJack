

from time import sleep
print("""
.------..------..------..------..------.     .------..------..------..------.
|B.--. ||L.--. ||A.--. ||C.--. ||K.--. |.-.  |J.--. ||A.--. ||C.--. ||K.--. |
| :(): || :/\: || (\/) || :/\: || :/\: ((5)) | :(): || (\/) || :/\: || :/\: |
| ()() || (__) || :\/: || :\/: || :\/: |'-.-.| ()() || :\/: || :\/: || :\/: |
| '--'B|| '--'L|| '--'A|| '--'C|| '--'K| ((1)) '--'J|| '--'A|| '--'C|| '--'K|
`------'`------'`------'`------'`------'  '-'`------'`------'`------'`------'
\n\n\n""")
sleep(3)
import random as r
from os import system

global num_of_decks
suits = {'S': '\u2660',
         'C': '\u2663',
         'H': '\u2665',
         'D': '\u2666'}

class Cards:
    def __init__(self, nod):
        card_num = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'J', 'Q', 'K']
        suits = ['S', 'C', 'H', 'D']
        self.deck = ([(idx, jdx) for idx in suits for jdx in card_num])
        self.deck = self.deck * nod
        r.shuffle (self.deck)

    def reshuffle_deck(self, nod):
        input ("Колодата е на път да завърши. Разместване на тесте. Натиснете произволен клавиш, за да продължите..")
        self.__init__ (nod)


class Hands:
    def __init__(self, player_onhand=pow (2, 25), is_dealer=False):
        self.dealer_hand = is_dealer
        self.cards = []
        self.value = 0
        self.ace = False
        self.player_current_balance = player_onhand
        self.bet = 0

    def win_bet(self):
        self.player_current_balance += self.bet

    def lose_bet(self):
        self.player_current_balance -= self.bet

    def add_card(self, card):
        self.cards.append (card)
        if card[1] == 'A':
            if not self.ace and (self.value + 11 <= 21):
                self.value = self.value + 11
                self.ace = True
            else:
                self.value = self.value + 1
        else:
            if type (card[1]) == int:
                self.value = self.value + card[1]
            else:
                self.value = self.value + 10
            if self.value > 21 and self.ace:
                self.value -= 10
                self.ace = False

    def print_card(self, card_suit, pos=1):
        s = ""
        for _ in card_suit:
            s = s + "\t ________"
        print (s.rjust (pos))
        s = ""
        for idx, jdx in card_suit:
            if jdx == 10:
                s = s + "\t| {0}     |".format (jdx)
            else:
                s = s + "\t| {0}      |".format (jdx)
        print (s.rjust (pos))
        s = ""
        for _ in card_suit:
            s = s + "\t|        |"
        print (s.rjust (pos))
        s = ""
        for idx, jdx in card_suit:
            s = s + "\t|   {0}    |".format (suits[idx])
        print (s.rjust (pos))
        s = ""
        for _ in card_suit:
            s = s + "\t|        |"
        print (s.rjust (pos))
        s = ""
        for idx, jdx in card_suit:
            if jdx == 10:
                s = s + "\t|     {0} |".format (jdx)
            else:
                s = s + "\t|      {0} |".format (jdx)
        print (s.rjust (pos))
        s = ""
        for _ in card_suit:
            s = s + "\t|________|"
        print (s.rjust (pos))

    def show_card(self, hide=False):
        if self.dealer_hand:
            if hide:
                print ('Дилър'.rjust (60))
                self.print_card ([self.cards[0]])
            else:
                print ('Дилър (Общо: {0})'.format (self.value).rjust (60))
                self.print_card (self.cards)
            for idx in range (4): print ('')
        else:
            print ('Играч (Общо: {0})'.format (self.value).rjust (60))
            self.print_card (self.cards)
            print ('Сума на залога: {0}'.format (self.bet).rjust (60))


def clear_screen():
    system ('cls')


def validate_number(p_text):
    while True:
        try:
            p_num = int (input (p_text))
        except ValueError:
            print ("Съжаляваме, моля, въведете номер")
        else:
            return p_num


def take_bet(player_hand):
    while True:
        player_hand.bet =validate_number('Колко чипа искате да заложите: ')
        if player_hand.bet > player_hand.player_current_balance:
            print ("За съжаление не можете да залагате повече от {0}".format (player_hand.player_current_balance))
        else:
            clear_screen ()
            break


def select_play_deck():
    global num_of_decks
    print ("Как могат тестета, с които искате да играете \n")
    num_of_decks = validate_number ("Изберете от номер 1 до 4:")
    while num_of_decks not in range (1, 5):
        clear_screen ()
        num_of_decks = int (input ("Невалиден избор. Моля, изберете от номер 1 до 4:"))
    clear_screen ()


print ('Добре дошли в Black Jack\n'.rjust (50))
select_play_deck ()
card = Cards (num_of_decks)

player_opening_balance = 100
play = 'Y'
while play in ("Y", "y"):
    dealer = Hands (is_dealer=True)
    player = Hands (player_opening_balance)
    take_bet (player)

    if len (card.deck) <= 7:
        card.reshuffle_deck (num_of_decks)
    for idx in range (2):
        player.add_card (card.deck.pop ())
        dealer.add_card (card.deck.pop ())
    dealer.show_card (True)
    player.show_card ()

    response = 2
    while response != 1:
        print ('')
        try:
            response = int (input ('Искате ли да останете (1) или да ударите (2)?: '))
            if response == 2:
                player.add_card (card.deck.pop ())
            system ('cls')
            dealer.show_card (True)
            player.show_card ()
            if player.value == 21:
                input ('Вашият общ сбор е 21. Останете на 21. Търн на дилъра. Натиснете произволен клавиш, за да продължите')
                break
            elif player.value > 21:
                break
        except:
            print ('Моля, въведете правилния номер')
            response = 0
    while dealer.value < 17 and player.value < 22:
        system ('cls')
        dealer.show_card (False)
        player.show_card ()
        print ('')
        print ('Общата сума на картите на дилъра е {0}. Дилърът се обръща, за да вземе картата \n'.format (dealer.value))
        input ('Натиснете произволен клавиш, за да продължите...')
        dealer.add_card (card.deck.pop ())
    system ('cls')
    dealer.show_card (False)
    player.show_card ()


    if player.value > 21:
        player.lose_bet ()
        print ('Дилърът има {0}, а Вие имате {1}. Дилърът СПЕЧЕЛИ!!'.format (dealer.value,
                                                                       player.value))
    elif dealer.value > 21:
        player.win_bet ()
        print (
            'Вие имате {0}, а дилърът има {1}. Вие СПЕЧЕЛИХТЕ!! ПОЗДРАВЛЕНИЯ'.format (player.value, dealer.value))
    elif dealer.value > player.value:
        player.lose_bet ()
        print ('Дилърът има общо {0} за карти. Дилърът спечели!!'.format (dealer.value))
    elif player.value > dealer.value:
        player.win_bet ()
        print ('Имате общо {0} за карти. Дилърът има общо {1} за карти. Вие спечелихте!! ПОЗДРАВЛЕНИЯ' \
               .format (player.value, dealer.value))
    else:
        print ("И двамата ви дилъри имат една и съща сума. Това е вратовръзка.")
    print ('')
    player_opening_balance = player.player_current_balance
    print ("Имате {0} чипа в ръка. \n".format (player_opening_balance))
    if player_opening_balance == 0:
        input ()
        play = 'N'
    else:
        play = input ('Искате ли да играете още? Да (Y) или Не (N)')
    clear_screen ()
else:
    print ("Благодаря, че играете с нас. Имате {0} чипа в ръката си. \n".format (player_opening_balance))
    input ("Натиснете произволен клавиш, за да съществувате...")
