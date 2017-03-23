import math
import random

class Pokemann:

    def __init__(self, name, kind, attack, defense, speed, health, catch_rate, moves, image):

        self.name = name
        self.kind = kind
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.health = health
        self.moves = moves # this is a list of Move objects
        self.image = image # path to image file
        self.fainted = False
        self.catch_rate = catch_rate
        
        self.current_health = health

        
    def get_available_moves(self):
        result = []
                  
        for m in self.moves:
            if m.remaining_power > 0:
                  result.append(m)

        else:
            pass
                    
        return result

    def get_random_move(self):
        available = self.get_available_moves()
        return random.choice(available)
    
    def execute_move(self, move, target):
        available = self.get_available_moves()

        if self.fainted:
            print("Error: " + self.name + " is fainted!")
        elif move not in available:
            print("Error: " + move.name + " is not available.")
        else:
            damage = move.get_damage(self, target)
            chance = random.randint(1,100)
            
            if chance <= move.accuracy:
                print(move.name + " hits " + target.name + " for " + str(damage) + ".")
                target.take_damage(damage)
            else:
                print(move.name + "missed!")

            move.remaining_power -= 1

    def take_damage(self, amount):
        self.current_health -= amount

        if self.current_health <= 0:
            self.faint()
            
    def faint(self):
        self.current_health = 0
        print(self.name + " fainted!")
        self.fainted = True
            
 
    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.health:
            self.current_health = self.health

        self.fainted = False
        print(self.name + "was healed. Health is now " + str(self.current_health) + "/" + str(self.health))
        
    def restore(self):
        self.current_health = self.health
        for move in self.moves:
            move.remaining_power = move.powerpoint
        print(self.name + " has been restored to full stats")

    def draw(self):
        pass
 

class Move:
    STRONG = 2.0
    NORMAL = 1.0
    WEAK = 0.5

    effectiveness = {
            ('reptile' ,'mammal'): STRONG,
            ('reptile' ,'reptile'): NORMAL,
            ('reptile', 'bird'): WEAK,
            ('mammal', 'bird'): STRONG,
            ('mammal' ,'mammal'): NORMAL,
            ('mammal' ,'reptile'): WEAK,
            ('bird' ,'reptile'): STRONG,
            ('bird', 'bird'): NORMAL,
            ('bird', 'mammal'): WEAK
          }


    def __init__(self, name, kind, powerpoint, power, accuracy):

        self.name = name
        self.kind = kind
        self.powerpoint = powerpoint
        self.power = power
        self.accuracy = accuracy
        self.remaining_power= powerpoint

    def calculate_damage(self, attacker, target):
        p = self.power
        a = attacker.attack
        d = target.defense
        e = self.effectiveness[(self.kind, target.kind)]
        
        return math.floor((((a*x)/50)-(d/10))*e)
    
    def restore(self):
        self.remaining_power = self.powerpoint
        print("Powerpoint restored")
        
class Character:
    
    def __init__(self, name, party, image):
        self.name = name
        self.party = party
        self.image = image
        
    def get_available_pokemann(self):
        result = []
            
        for a in self.party:
            if a.fainted == False:
                result.append(a)

            elif a.fainted == True:
                pass

        return result
    
    def get_active_pokemann(self):
        """
        Returns the first unfainted character in the pokemann list. If all pokemann
        are fainted, return None.
        """
        available = self.get_available_pokemann()

        if len(available) > 0:
            return available[0]
        else:
            return None
    
    '''def set_first_pokemann(self, swap_pos):
        self.available[0], self.available[swap_pos]= self.available[swap_pos], self.available[0]
        '''
    def restore(self):
        for p in self.party:
            p.restore()
            
    def draw(self):
        pass
    
'''class Game:

    def __init__(self):
        pass

    def select_pokemann(character):
        nums= 1
        for a in character.pokemann:
            if a.fainted == True:
                print(str(nums) + ")" + a.name + ": Fainted")
                nums+= 1
            else:
                print(str(nums) + ")" + a.name + ": " + str(a.health))
                nums+=1

        pokemannnum=int(input("Select a Pokemann to battle (number): "))-1
        character.get_available_pokemann()
        character.get_first_pokemann()
        character.set_first_pokemann(pokemannnum)
        return character.available

    def select_random_pokemann(self, character):
        pokes = character.get_available_pokemann()
        return random.choice(poke)
    
    def select_move(pokemann):
        available = pokemann.get_available_moves()
        
        print("Select a move:")
        
        for i, move in enumerate(available):
            print(str(i) + ") " + move.name)

        n = input("Your choice: ")
        n = int(n)
        
        return available[n]

    def select_random_move(pokemann):
        available_moves = pokemann.get_available_moves()
        return random.choice(available_moves)

    def fight(player_pokemann, target_pokemann):
        """
        This controls the logic for a single round in a fight whether in context of a battle
        or with a wild pokemann.
        
        1. Select player_move (use select_move)
        2. Select target_move (use select_random_move)
        3. Compare speeds of player_pokemann and target_pokemann
            If player_pokemann.speed > target_pokemann.speed, set first = player_pokemann,
            second = target_pokemann. Otherwise, set first = target_pokemann, second = player_pokemann
            If speeds are equal, assign first and second randomly.
        4. Call
            first.execute_move(move, second)
        5. If second is still unfainted, call
            second.execute_move(move, first)
        (Once we have an actual game, we'll need to devise a way to remove fainted targets.)
        """
        if player_pokemann.fainted == False and target_pokemann.fainted == False:
            player_move = Game.select_move(player_pokemann)
            random_move = Game.select_random_move(target_pokemann)
            if player_pokemann.speed > target_pokemann.speed:
                first= player_pokemann
                second= target_pokemann
            elif player_pokemann.speed < target_pokemann.speed:
                first= target_pokemann
                second= player_pokemann
            else:
                poke=  [target_pokemann, player_pokemann]
                first = random.choice(poke)
                poke.remove(first)
                second = poke[0]
            first.execute_move(player_move, second)
            if second.fainted == False:
                second.execute_move(random_move, first)
            else:
                print(second + " has fainted")
                
            if first.fainted == True:
                print(first + " has fainted")'''
            
class Player(Character):

    def __init__(self, name, party, image):
        Character.__init__(self, name, party, image)

        self.computer = []
        self.pokeballs = 0

    def catch(self, target):
        """
        Can only be applied to a wild pokemann. Determine a catch by generating a random
        value and comparing it to the catch_rate. If a catch is successful, append the
        target to the player's pokemann list. However, if the pokemann list already
        contains 6 pokemann, add the caught target to the players computer instead.
        Pokemann sent to the computer will be fully restored, but other caught pokemann
        will remain at the strength they were caught. Decrease the player's pokeball
        count by 1 regardless of success.
        Return True if the catch is successful and False otherwise.
        """
        r = random.randint(1, 100)

        if r <= target.catch_rate:
            print("Congratulations! You just caught a " + target.name + " !")
            
            if len(self.party) < 6:
                self.party.append(target)
                print(target.name + " has been added to your party!")
                target.restore()
            elif len(self.party) == 6:
                self.computer.append(target)
                print(target.name + " has been put in your locker.")
                target.restore()
        else:
            print("It got away!")
            
        
    def run(self, target):
        """
        Can only be applied in the presence of a wild pokemann. Success is determined by
        comparing speeds of the player's active pokemann and the wild pokemann. Incoroporate
        randomness so that speed is not the only factor determining success.
        Return True if the escape is successful and False otherwise.
        """
        self.get_active_pokemann()
        p = available[0]
        r = random.randint(-30, 30)
        if p.speed + (2*r) > target.speed + r:
            return True
        else:
            return False
    
   
class NPC(Character):

    def __init__(self, name, party, image):
        Character.__init__(self, name, party, image)
      

class Game:

    def __init__(self):
        pass
    



if __name__ == '__main__':

    # Make some moves
    talon_scratch = Move('Talon Scratch', 'bird', 20, 15, 100)
    aerial_strike = Move('Aerial Strike', 'bird', 15, 20, 90)
    sonic_boom = Move('Sonic Boom Screech', 'bird', 20, 13, 100)
    egg_bomb = Move('Egg Bomb', 'bird', 5, 25, 80)

    bite = Move('Bite', 'mammal', 25, 15, 100)
    claw_attack = Move('Claw Attack', 'mammal', 20, 20, 90)
    tackle = Move('Tackle', 'mammal', 20, 20, 85)
    furball_cannon = Move('Furball Cannon', 'mammal', 5, 25, 80)

    poison_sting = Move('Poison Sting', 'reptile', 15, 20, 95)
    shed_skin = Move('Shed Skin', 'reptile', 15, 0, 100)
    sharp_scales =  Move('Sharp Scales', 'reptile', 10, 20, 90)
    spit_fire = Move('Spit Fire', 'reptile', 5, 25, 80)


    # Create some Pokemann(s)
    blessed_little_goose = Pokemann('Blessed Little Goose', 'bird', 23, 78, 15, 145, 75, [aerial_strike, egg_bomb, bite, furball_cannon], 'none')
    american_spirit_eagle = Pokemann('American Spirit Eagle', 'bird', 81, 18, 76, 122, 20, [sonic_boom, aerial_strike, spit_fire, talon_scratch], 'none')
    pedro_the_imported_platypus = Pokemann('Pedro The Imported Platypus', 'mammal', 65, 21, 48, 162, 25, [egg_bomb, bite, poison_sting, claw_attack], 'none')
    baaaa_goat = Pokemann('Baa Goat', 'mammal', 90, 10, 47, 107, 60, [bite, spit_fire, furball_cannon, aerial_strike], 'none') 
    blek_the_snek = Pokemann('Blake the Snake', 'reptile', 57, 39, 100, 100, 5, [spit_fire, egg_bomb, bite, poison_sting], 'none')
    teenage_mutant_ninja_daddy = Pokemann('Teenage Mutant Ninja Daddy', 'reptile', 8, 100, 8, 210, 40, [shed_skin, egg_bomb, bite, poison_sting], 'none')

    # Create Player
    casey = Player("Casey Katch-em-all", [blessed_little_goose, pedro_the_imported_platypus, blek_the_snek], "casey.png")
    river = Player("River the Radical", [baaaa_goat, american_spirit_eagle, teenage_mutant_ninja_daddy], "river.png")

    # Create NPCs

    # Create a Game
    g = Game()
