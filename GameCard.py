from random import *
from math import *
from time import *
from Settings import *

class GameCard:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, colors= Colors, values=Values32) -> None:
        self.Colors = colors
        self.Values = values
        self.Game = self.create_game(self.Colors, self.Values)

        # display cpd = Card Per View
        self.cpd = 8

    def __str__(self) -> str:
        return  str(Card.__str__(Card(), self.Game, cardPerView=self.cpd))

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    #--------------------------------------------------------------- Helper Functions ---------------------------------------------------------------#

    def create_game(self, colors: tuple, values: tuple) -> list:
        return [Card(c, v) for c in colors for v in values]
    
    def shuffling(self) -> None:
        return shuffle(self.Game)

    def drawing(self, where='top') -> object:
        if where == 'top':
            return self.Game.pop(0)
        elif where == 'bottom':
            return self.Game.pop(len(self.Game)-1)
        elif where == 'random':
            return self.Game.pop(randint(0, len(self.Game))-1)
        else:
            return self.Game.pop(int(where))

    def create_hand(self, ncard=2, where='top') -> list: 
        return [self.drawing(where) for _ in range(ncard)]

    def get_forcecard(self, card: object) -> int:
        assert isinstance(card, Card), 'Your input is not a Card'
        
        if card.Value == None:
            return 0
        elif card.Value == 'A':
            return 14
        elif card.Value == 'K':
            return 13
        elif card.Value == 'Q':
            return 12
        elif card.Value == 'J':
            return 11
        else:
            return int(card.Value)

    def get_forceval(self, val: str) -> int:
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def get_sum_force(self, Hand: object) -> int:
        s = 0
        for card in Hand:
            s =+ self.get_forcecard(card)
        return s

    def get_lowerforce(self) -> int:
        val = self.Values[0]
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def get_higherforce(self) -> int:
        val = self.Values[-1]
        if val == 'A':
            return 14
        elif val == 'K':
            return 13
        elif val == 'Q':
            return 12
        elif val == 'J':
            return 11
        else:
            return int(val)

    def compare(self, card1: object, card2: object) -> (object | bool):
        assert isinstance(card1, Card) and isinstance(card2, Card), 'Your input(s) is(are) not a Card'

        a = self.get_forcecard(card1)
        b = self.get_forcecard(card2)
        if a > b:
            return card1
        elif b > a:
            return card2
        elif a == b:
            return None

    def Check(self, Hand: list, display=True) -> (tuple | str):
        Deck = Hand + self.Board
        occ = self.ValueOccurence(Deck)
        occ = self.SortOccurence(occ)
        straight = self.Straight(Deck, finder=True)
        flush = self.Flush(Deck, finder=True)

        if (flush != None and straight != None) and self.StraightFlush(flush, straight) != None:
            check = (self.StraightFlush(flush, straight), 'Straight Flush', 9) # Straight Flush
            if self.RoyaleFlush(check[0]) != None:
                check = (self.RoyaleFlush(check[0]), 'Royale Flush !', 10) # Royale Flush !
        elif len(occ) == 1 and occ[0][1] == 4:
            check = (self.ComboOcc(Deck, occ), 'Four of kind', 8) # Four of kind
        elif len(occ) == 2 and (occ[0][1] == 3 and occ[1][1] == 2):
            check = (self.ComboOcc(Deck, occ), 'Full House', 7) # Full House
        elif flush != None:
            check = (self.Flush(Deck), 'Flush', 6) # Flush
        elif straight != None:
            check = (self.Straight(Deck), 'Straight', 5) # Straight
        elif len(occ) == 1 and occ[0][1] == 3:
            check = (self.ComboOcc(Deck, occ), 'Tree of kind', 4) # Tree of kind
        elif len(occ) == 2 and (occ[0][1] == 2 and occ[1][1] == 2):
            check = (self.ComboOcc(Deck, occ), 'Double Pair', 3) # Double Pair
        elif len(occ) == 1 and occ[0][1] == 2:
            check = (self.HighPair(Deck), 'Pair', 2) # Pair
        else:
            check = (self.HighCard(Deck), 'High Card', 1) # High Card

        if display:
            if isinstance(check[0], Card):
                return f'{check[1]} :\n\n{check[0]}'
            else:
                return f'{check[1]} :\n\n{Card.__str__(self, check[0], 5)}'
        else:
            return check

    def ValueOccurence(self, Deck: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Deck = self.sortAscending(Deck, reverse=True)
        occurence = []
        for i in range(2, 14+1):
            n = 0
            for card in Deck:
                if self.get_forcecard(card) == i:
                    n += 1
                    value = card.Value
            if n >= 2:
                occurence.append((value, n))
        return occurence

    def SortOccurence(self, occurence: list) -> list:
        sortedocc = []
        for n in range(2, 4+1):
            append = False
            occ = []
            for i in range(len(occurence)):
                if occurence[i][1] == n:
                    occ.append(occurence[i])
                    append = True
            if append:
                sortocc = []
                for l in range(2, 14+1):
                    for k in range(len(occ)):
                        if self.get_forceval(occurence[k][0]) == l:
                            sortocc.append(occurence[k])
                sortedocc += sortocc
        sortedocc.reverse()
        if len(sortedocc) == 3:
            sortedocc.pop(2)
        elif len(sortedocc) == 2:
            if sortedocc[0][1] == 4 and sortedocc[1][1] == 3:
                sortedocc.pop(1)
            elif sortedocc[0][1] == 3 and sortedocc[1][1] == 3:
                sortedocc[1][1] = 2
        return sortedocc

    def ComboOcc(self, Deck: list, occ: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'
        assert not len(occ) == 0, 'Your occurence list is empty'

        combo = []
        for i in range(len(occ)):
            for card in Deck:
                if card.Value == occ[i][0]:
                    combo.append(card)
        return combo

    def ColorOccurrence(self, Deck: list) -> list:
        Deck = self.sortAscending(Deck, reverse=True)
        occurence = []
        for color in self.Colors:
            n = 0
            for card in Deck:
                if card.Color == color:
                    n += 1
            if n >= 5:
                occurence.append((color, n))
        return occurence

    #----------------------------------------------------------------- Cards Combos -----------------------------------------------------------------#

    def HighCard(self, Deck: list) -> object:
        assert not len(Deck) == 0, 'Your Deck is empty'

        High = Deck[0]
        for card in Deck:
            if self.get_forcecard(card) > self.get_forcecard(High):
                High = card
        return High

    def LowCard(self, Deck: list) -> object:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Low = Deck[0]
        for card in Deck:
            if self.get_forcecard(card) < self.get_forcecard(Low):
                Low = card
        return Low

    def HighPair(self, Deck: list) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        Deck = self.sortAscending(Deck, reverse=True)

        for i in range(len(Deck)-1):
            for j in range(i+1, len(Deck)):
                if Deck[i].Value is Deck[j].Value:
                    return [Deck[i], Deck[j]]

    def Straight(self, Deck: list, finder=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'
        assert len(Deck) >= 5, 'Your Deck must have 5 cards'

        Check = []

        for card in Deck:
            canappend = True
            for occ in Check:
                if card.Value == occ.Value:
                    canappend = False
            if canappend:
                Check.append(card)

        Check = self.sortAscending(Check, reverse=True)
        AllStraight = []

        if len(Check) < 5:
            return None

        for i in range(len(Check)):
            Straight = []
            Straight.append(Check[i])

            for j in range(1, 4+1):
                
                try:
                    if self.get_forcecard(Check[i+j]) == self.get_forcecard(Check[i])-j:
                        Straight.append(Check[i+j])
                except IndexError:
                    if self.get_forcecard(Check[(i+j)-len(Check)]) == self.get_forcecard(Check[i])+(self.get_higherforce() - self.get_lowerforce())-j+1:
                        Straight.append(Check[i+j-len(Check)])

            if len(Straight) == 5:
                for card in Straight:
                    if card not in self.Board:
                        if finder == False:
                            return Straight
                        AllStraight.append(Straight)
        if finder:
            if AllStraight == []:
                return None
            return AllStraight
        return None

    def Flush(self, Deck: list, finder=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        flush = self.ColorOccurrence(Deck)

        if flush == []:
            return None

        combo = []
        for i in range(len(flush)):
            for card in Deck:
                if card.Color == flush[i][0]:
                    combo.append(card)

        combo = self.sortAscending(combo)
        if finder:
            return combo

        if len(combo) == 5:
            for card in combo:
                if card not in self.Board:
                    return combo
        else:
            while len(combo) != 5:
                canremove = True
                for card in combo:
                    if card in self.Board and canremove == True:
                        combo.remove(card)
                        canremove = False
            return combo
        
    def StraightFlush(self, flush: list, straight: list) -> (list | None):
        assert flush is not None, "flush can't be a NoneType"
        assert straight is not None, "straight can't be a NoneType"

        for i in range(len(straight)):
            straightflush = []
            for card in straight[i]:
                if card not in flush:
                    break
                straightflush.append(card)
            if len(straightflush) == 5:
                return straightflush
        return None

    def RoyaleFlush(self, Deck: list) -> (list | None):
        assert len(Deck) == 5, 'Your Deck should be an StraightFlush'

        Deck = self.sortAscending(Deck, reverse=True)

        if Deck[0].Value == 'A' and Deck[1].Value == 'K' and Deck[2].Value == 'Q' and Deck[3].Value == 'J' and Deck[4].Value == '10':
            return Deck
        return None


class Card:

    def __init__(self, color=None, value=None) -> None:
        self.Color = color
        self.Value = value

    def __str__(self, gamecard=None, cardPerView=5, up='', mid='', down='') -> str:
        char = ''
        if isinstance(gamecard, list):
            for i in range(1, len(gamecard)+1):
                assert isinstance(gamecard[i-1], Card), 'There is something that is not a card in your game'

                card = gamecard[i-1].str_card()
                up += card[0] + '  '
                mid += card[1] + '  '
                down += card[2] + '  '

                if i%cardPerView == 0:
                    up += '\n'
                    mid += '\n'
                    down += '\n\n'
                    char += up + mid + down
                    up = ''
                    mid = ''
                    down = ''
                elif i == len(gamecard):
                    up += '\n'
                    mid += '\n'
                    down += '\n\n'
                    char += up + mid + down
        else:
            card = self.str_card()
            char += card[0] + '\n'
            char += card[1] + '\n'
            char += card[2] + '\n\n'
        return char

    def str_card(self) -> tuple:
        # Up value
        if len(self.Value) == 1:
            up = '|' + self.Value + '   ' + self.Value + '|'
        elif len(self.Value) == 2:
            up = '|' + self.Value + ' ' + self.Value + '|'

        # Symbole de Couleur
        if self.Color == 'Pique':
            mid = '|  ♠  |'
        elif self.Color == 'Trèfle':
            mid = '|  ♣  |'
        elif self.Color == 'Coeur':
            mid = '|  ♥  |'
        elif self.Color == 'Carreau':
            mid = '|  ♦  |'
        
        # Down value
        if len(self.Value) == 1:
            down = '|' + self.Value + '   ' + self.Value + '|'
        elif len(self.Value) == 2:
            down = '|' + self.Value + ' ' + self.Value + '|'
            
        return (up, mid, down)

class Poker(GameCard):

    def __init__(self, colors=Colors, values=Values32) -> None:
        super().__init__(colors, values)
        self.Board = None
        
        # Players and Bots
        self.Pot = 0
        self.Blind = 10
        self.Max_amount = 0

        self.Players = [Bot(f'Bot{i}') for i in range(1, 7+1)]
        self.Players.append(Player())

    def __str__(self) -> str:
        return super().__str__()

    def __call__(self) -> None:
        return self.run()

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    #--------------------------------------------------------------- Helper Functions ---------------------------------------------------------------#

    def sortAscending(self, Deck: list, reverse=False) -> list:
        assert not len(Deck) == 0, 'Your Deck is empty'

        sortedlist = []
        if reverse == True:
            for i in range(self.get_forcecard(self.HighCard(Deck))+1, self.get_forcecard(self.LowCard(Deck))-1, -1):
                for cards in Deck:
                    if self.get_forcecard(cards) == i:
                        sortedlist.append(cards)
        else:
            for i in range(self.get_forcecard(self.LowCard(Deck)), self.get_forcecard(self.HighCard(Deck))+1):
                for cards in Deck:
                    if self.get_forcecard(cards) == i:
                        sortedlist.append(cards)
        return sortedlist

    def defindBlind(self) -> None:
        assert len(self.Players) >= 2, 'Play alone is borring'

        n=0
        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                try:
                    self.Players[i+1].Blind = 'BigBlind'
                except IndexError:
                    self.Players[i-len(self.Players)+1].Blind = 'BigBlind'
                self.Players[i].Blind = 'SmallBlind'
                self.Players[i-1].Blind = None
                break      
            elif self.Players[i].Blind == None:
                n+=1
        if n == len(self.Players):
            self.Players[-1].Blind = 'BigBlind'
            self.Players[-2].Blind = 'SmallBlind'

        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                self.Players[i].Bank -= self.Blind
                self.Players[i].Bet += self.Blind

            if self.Players[i].Blind == 'SamllBlind':
                self.Players[i].Bank -= self.Blind//2
                self.Players[i].Bet += self.Blind//2

        self.Max_amount = self.Blind

    def Compare(self, player_1: object, player_2: object) -> (object | str):
        assert isinstance(player_1, Player) or isinstance(player_1, Bot), 'Your Player1 isn\'t a Player or Bot'
        assert isinstance(player_2, Bot) or isinstance(player_2, Player), 'Your Player2 isn\'t a Player or Bot'

        check_1 = self.Check(player_1.Deck, display=False)
        check_2 = self.Check(player_2.Deck, display=False)
        if check_1[2] > check_2[2]:
            return player_1
        elif check_2[2] > check_1[2]:
            return player_2
        elif check_1[2] == check_2[2]:
            if check_1[2] == 0 and check_2[2] == 0:
                results = GameCard.compare(self, check_1[0], check_2[0])
                if results is check_1[0]:
                    return player_1
                elif results is check_2[0]:
                    return player_2
                else:
                    return 'Equality !'
            a, b = 0, 0
            for card_1 in check_1[0]:
                a += GameCard.get_forcecard(self, card_1)
            for card_2 in check_2[0]:
                b += GameCard.get_forcecard(self, card_2)
            if a > b:
                return player_1
            elif b > a:
                return player_2
            else:
                return 'Equality !'

    def displayinfo(self) -> None:
        if len(self.Board) != 0:
            print(Card.__str__(self, self.Board))
            print(Spare)
        print(self.Players[-1])
        if len(self.Board) >= 3:
            print(self.Check(self.Players[-1].Deck, self.Board))

    #_____________________________________________________________________ Main _____________________________________________________________________#

    def reset(self) -> None:
        self.Game = GameCard(self.Colors, self.Values)

        for players in self.Players:
            players.Deck = None
            players.Bet = 0

        self.Pot = 0
        self.Max_amount = 0
        self.Board = self.Game.create_hand(0)

    def initialisation(self) -> None:
        self.reset()
        self.Game.shuffling()
        self.cpd = 14

        for players in self.Players:
            players.Deck = self.Game.create_hand(2, where='bottom')

        self.defindBlind()

    def biddingRound(self) -> None:
        
        for i in range(len(self.Players)):
            if self.Players[i].Blind == 'BigBlind':
                if i+1 > len(self.Players)-1:
                    utg = i-len(self.Players)+1
                else:
                    utg = i+1

        AllCheck = True
        OneLoop = False

        while True:
            havefold = False
            haveraise = False

            if self.Players[utg].State != 'Fold' and self.Players[utg].All_in == False:

                if self.Players[utg].Bet == self.Max_amount:
                    self.Players[utg].CanCheck = True
                    self.Players[utg].CanCall = False
                else:
                    self.Players[utg].CanCheck = False
                    self.Players[utg].CanCall = True
    

                choice = self.Players[utg].choice()

                if choice != 'Check':
                    AllCheck = False
                
                if choice == 'Call':
                    diff = self.Max_amount - self.Players[utg].Bet
                    if diff == self.Players[utg].Bank:
                        self.Players[utg].All_in = True # All-in
                    elif diff >= self.Players[utg].Bank:
                        self.Players[utg].All_in = True # All-in Partial

                    if diff < self.Players[utg].Bank:
                        self.Players[utg].Bet += diff
                        self.Players[utg].Bank -= diff
                    else:
                        self.Players[utg].Bet += self.Players[utg].Bank
                        self.Players[utg].Bank = 0

                elif choice == 'Raise':
                    r = self.Players[utg].raising()
                    if r == self.Players[utg].Bank:
                        self.Players[utg].All_in = True

                    self.Max_amount += r
                    self.Players[utg].Bet += r
                    self.Players[utg].Bank -= r
                    haveraise = True

                elif choice == 'Fold':
                    havefold = True

            char = f'{self.Players[utg].Name} have: {self.Players[utg].State}'

            if haveraise:
                char += f' of {r}.'
            if self.Players[utg].All_in == True:
                char += ' All in !'

            char += f'\n\nMax Amount: {self.Max_amount} Pot : {self.Pot}'

            if self.Players[utg].State != 'Fold' or havefold:
                print(char)
                print(Spare)
                sleep(1)
            
            if self.Players[utg].Blind == 'BigBlind':
                OneLoop = True
                if AllCheck:
                    break
            
            if OneLoop:
                Same_Amount = True
                All_All_In = True
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if self.Players[i].All_in == False:
                            All_All_In = False
                            break
                if All_All_In:
                    break
                max_bet = 0
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if self.Players[i].Bet > max_bet:
                            max_bet = self.Players[i].Bet
                for i in range(len(self.Players)):
                    if self.Players[i].State != 'Fold':
                        if not(self.Players[i].All_in):
                            if max_bet != self.Players[i].Bet:
                                Same_Amount = False
                                break
                        elif self.Players[i].All_in:
                            if not(self.Players[i].Bet <= max_bet):
                                Same_Amount = False
                                break
                if Same_Amount:
                    break
                
            if utg == len(self.Players)-1:
                utg = (utg-len(self.Players))+1
            else:
                utg += 1

        for i in range(len(self.Players)):
            self.Pot += self.Players[i].Bet
            self.Players[i].Bet = 0
        self.Max_amount = 0

    def win(self) -> None:
        for players in self.Players:
            if players.State != 'Fold':
                print(f'{players.Name} :\n')
                print(Card.__str__(self, players.Deck))
                print(self.Check(players.Deck))
                print(Spare)

        winner = []
        for i in range(len(self.Players)):
            if self.Players[i].State != 'Fold' and len(winner) != 0:
                win = self.Compare(self.Players[i], winner[0])

                if win is self.Players[i]:
                    winner = []
                    winner.append(self.Players[i])
                elif win == 'Equality !':
                    winner.append(self.Players[i])

            elif self.Players[i].State != 'Fold' and len(winner) == 0:
                winner.append(self.Players[i])
        
        for win in winner:
            win.Bank += self.Pot // len(winner)

        if len(winner) == 1:
            print(f'{winner[0].Name} win the game, an the pot of {self.Pot}!')
        else:
            char = ''
            for i in range(len(winner)):
                char += f'{winner[i].Name}, '
            print(f'The winners are {char} !')

    def flop(self) -> None:
        for _ in range(3):
            self.Board.append(self.Game.drawing())

    def turn(self) -> None:
        self.Board.append(self.Game.drawing())

    def river(self) -> None:
        self.Board.append(self.Game.drawing())

    #--------------------------------------------------------------------- Runs ---------------------------------------------------------------------#
    
    def run(self) -> None:
        self.initialisation()

        self.displayinfo()
        self.biddingRound()
        self.flop()
        self.displayinfo()
        self.biddingRound()
        self.turn()
        self.displayinfo()
        self.biddingRound()
        self.river()
        self.displayinfo()
        self.biddingRound()

        self.win()

    #-------------------------------------------------------------------- States --------------------------------------------------------------------#

class Player:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, name='Player', deck=None) -> None:
        self.Name = name
        self.Deck = deck
        self.Score = 0
        self.Bank = 1000
        self.Blind = None
        self.State = None
        self.Bet = 0
        self.All_in = False
        self.CanCheck = True
        self.CanCall = True

    def __str__(self) -> str:
        return f'\nHand of the {self.Name}:\n\n{Card.__str__(self, self.Deck)}Bank : {self.Bank}\n\n'

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    def choice(self) -> str:
        print('Check: 1, Call: 2, Raise: 3, Fold: 4')
        print(Spare)
        while True:
            c = None
            try:
                c = int(input('Make your descision: '))
                print(Spare)
            except ValueError:
                print(f'Your input {c} is not a number')
                continue
            if 1 <= c and c <= 4:
                if c == 1:
                    if self.CanCheck:
                        self.State = 'Check'
                    else:
                        print('You can\'t check')
                        continue
                elif c == 2:
                    if self.CanCall:
                        self.State = 'Call'
                    else:
                        print('You can\'t call')
                        continue
                elif c == 3:
                    self.State = 'Raise'
                elif c == 4:
                    self.State = 'Fold'

                return self.State
            else:
                print('Your number must be bettween 1 and 4')

    def raising(self) -> int:
        print(Spare)
        while True:
            r = None
            try:
                r = int(input(f'How many would you raise ?\nBank : {self.Bank}\n'))
                print(Spare)
            except ValueError:
                print(f'Your input {r} is not a number')
                continue

            if r <= self.Bank:
                return r
            else:
                print(f'Your number must be bettween 1 and {self.Bank}')

class Bot:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, name='Bot', punder=random(), deck=None) -> None:
        self.Name = name
        self.Deck = deck
        self.Score = 0
        self.Bank = 1000
        self.Blind = None
        self.State = None
        self.Bet = 0
        self.All_in = False
        self.CanCheck = True
        self.CanCall = True

        self.iter = 16

        # self.Bluff = bluff                  # Honest    0%------100%    Liar
        self.Punder = punder*2                # Thrifty   0%------100%    Spendthrifty
        # self.Carefulness = carefulness      # Naive     0%------100%    Careful

    def __str__(self) -> str:
        return f'\nHand of the {self.Name}:\n\n{Card.__str__(self, self.Deck)}Bank : {self.Bank}\n\n'

    #______________________________________________________________ Specials Functions ______________________________________________________________#

    def choice(self) -> str:
        issues = {'Check': 0, 'Call': 0, 'Raise': 0, 'Fold': 0}

        for i in range(self.iter):
            r = random()
            if 0 <= r and r < 1/6:
                issues['Fold'] += 1
            elif 1/6 <= r and r < 3/6 and self.CanCheck:
                issues['Check'] += 1
            elif 3/6 <= r and r < 5/6 and self.CanCall:
                issues['Call'] += 1
            elif 5/6 <= r and r <= 1:
                issues['Raise'] += 1

        all_m = []
        for ch in issues:
            issues[ch] = (issues[ch]/self.iter)*100
            all_m.append(issues[ch])
        m = max(all_m)
        # print(issues)

        if isclose(m, issues['Check']):
            state = 'Check'
        elif isclose(m, issues['Call']):
            state = 'Call'
        elif isclose(m, issues['Raise']):
            state = 'Raise'
        elif isclose(m, issues['Fold']):
            state = 'Fold'

        self.State = state
        return state

    def raising(self) -> int:
        r = randint(0, self.Bank)/self.Bank
        if 0 <= r and r <= self.Punder/2:
            r = randint(0, self.Bank//10)
        elif self.Punder/2 < r and r < self.Punder:
            r = randint(0, self.Bank)
        elif (self.Punder <= r and r <= 2) and self.Punder >= 1.6:
            r = self.Bank
        else:
            r = randint(0, self.Bank//(4/3))
        return r

if __name__ == '__main__':
    Game = Poker()
    Game()