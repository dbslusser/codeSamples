"""

Description:
    This app simulates a bowling game. When prompted, enter the number of pins
    knocked down by the player for the frame/roll specified. 
        Enter 'p' anytime during the game to see the current score.
        Enter 'q' anytime during the game to end. 

Parameters:
    player - name of player
    frames - number of frames to play

Example:
    bowl.py --player clay --player david --frames 10
    
"""

__version__ = "0.0.1"


import sys
import argparse
from cmd import Cmd


def Opts():
    """ Return an argparse object. """
    parser = argparse.ArgumentParser(description = __doc__,
                          formatter_class=argparse.RawTextHelpFormatter)    
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--frames', type=int, default=10, required=False, help='set the number of frames in a game')    
    parser.add_argument('--player', action="append", default=[], help='add a bowler to the game')  
    args = vars(parser.parse_args())
    return type("Opts", (object,), args)


class Player:
    """
    Description:
        Represents a Player in a bowling game 
    
    Parameters:
        name - name of bowler
    """
    def __init__(self, name):
        """ Class entry point """
        self.name = name
        self.frames = []

    def score(self):
        """
        Description:
            Calculate score
        
        Returns:
            players current total score as an integer
        """
        return sum([f.score for f in self.frames if f.score])

    def __repr__(self):
        """ str representation of a players name """
        return self.name


class Frame:
    """
    Description:
        Represents a single frame in the game 
    
    Parameters:
        rolls      - number of rolls in turn  
        prev_frame - previous frame
    """
    def __init__(self, rolls=[], previous_frame=None):
        """ Class entry point """
        self.rolls = rolls
        self.previous_frame = previous_frame
        self.calculateScore()

    def calculateScore(self, rolls=[]):
        """ 
        Description:
            calculate bowling score; determine
        
        Parameters:
            rolls - list of balls in future frames (for stike/spare calculations)
        """
        # add the next frames rolls to this frames rolls
        rolls = self.rolls + rolls
        if self.previous_frame:
            if not self.previous_frame.score:
                self.previous_frame.calculateScore(rolls)
        
        # calculate with strike
        if len(rolls) >= 3 and self.isStrike:
            self.score = sum(rolls[:3])
        
        # calculate with spare
        elif len(rolls) >= 3 and self.isSpare:
            self.score = sum(rolls[:3])
        
        # calculate frame
        elif not self.isSpare and not self.isStrike:
            self.score = sum(self.rolls)
        
        else:
            self.score = None

    @property
    def formatScore(self):
        """
        Description:
            Convert frame score to bowling format (X for strike; / for spare; - for gutter)

        Returns:
            bowling formated frame score as string
        """
        disp = self.rolls[:]
        # check for spares
        if len(disp) > 2:
            if sum(disp[:2]) == 10 and disp[0] < 10:
                disp[1] = "/"
            elif sum(disp[-2:]) == 10 and disp[1] < 10 and disp[2] < 10:
                disp[2] = "/"

        elif self.isStrike: return "X"
        elif self.isSpare: return "%s /" % disp[0]
        return " ".join(str(r) for r in disp).replace("10", "X").replace("0", "-")

    @property
    def isSpare(self):
        """ return true if spare """
        if not self.isStrike and sum(self.rolls) == 10:
            return True

    @property
    def isStrike(self):
        """ return true if strike """
        if self.rolls[0] == 10:
            return True

    def __repr__(self):
        return "%s" % self.rolls


class Game:
    """ 
    Description:
        Represents a game of bowling, tracking state and uses players/frames.
    
    Parameters:
        players - list of players objects
    """
    round = []
    ball = 0
    turn = 0
    frame = 0
    finished = False

    def __init__(self, players, total_frames=10):
        """ Class entry point """
        self.players = players
        self.bowler = players[0]
        self.ball = 0
        self.frame = 0
        self.total_frames = total_frames
        self.total_players = len(players)

    def playTurn(self, pins):
        """
        Description:
            Tracks a players turn, tallies pins knocked down but rolls(1 or 2)
        
        Parameters:
            pins - number of pins knocked down
        """
        previous_frame = self.bowler.frames[-1] if self.frame > 0 else None
        self.bowler.frames.append(Frame(self.round + [pins], previous_frame))
        self.setupTurn()
        if self.frame == self.total_frames:
            self.finished = True

    def setupTurn(self):
        """ Reset variables and counters for next bowler """
        self.turn = (self.turn + 1) % self.total_players
        self.bowler = self.players[self.turn]
        if self.turn == 0:
            self.frame += 1
        self.ball = 0
        self.round = []

    def talleyPins(self, pins):
        """
        Description:
            talley pins knocked down for a roll
        
        Parameters:
            pins - number of pins knocked down
        """
        if self.ball == 0:
            if pins == 10:
                if self.frame == self.total_frames-1:
                    self.round = [pins]
                    self.ball += 1
                else:
                    self.playTurn(pins)
            else:
                self.round = [pins]
                self.ball += 1

        elif self.ball == 1:
            if self.frame == self.total_frames-1 and self.round[0] == 10:
                self.round += [pins]
                self.ball += 1
                return
            if pins == 10:
                if self.frame == self.total_frames-1:
                    if self.round[0] == 10:
                        self.round += [pins]
                    else:
                        self.round += [10 - self.round[0]]
                    self.ball += 1
                else:
                    self.playTurn(10 - self.round[0])
            elif self.round[0] + pins <= 10:
                if self.frame == self.total_frames-1:
                    if (self.round[0] + pins) == 10:
                        self.ball += 1
                        self.round += [pins]
                        return
                self.playTurn(pins)
            else:
                raise ValueError

        elif self.ball == 2:
            self.playTurn(pins)

    def getScores(self):
        """ Compile scores of frames played """
        results = ""
        for p in self.players:
            results += ('\n'.join([
                "\n%s: \t%s" % (p.name, p.score()),
                "-" * 7 * len(p.frames),
                " | ".join([str(f.formatScore).rjust(5) for f in p.frames]),
                " | ".join([str(f.score).rjust(5) for f in p.frames]),
                ""
            ]))
        return results


class GameLoop(Cmd):
    """
    Description:
        Bowling game input loop. Ask for number of pins that were knocked down on each roll. 
    
    Parameters:
        game - bowling game object
    """
    intro = """Enter the number pins the player knocks down. 
   Enter 'p' to print the scoreboard. 
   Enter 'q' to end the game. 
            """
    def __init__(self, game):
        """ Class entry point """
        self.game = game
        self.setupprompt()
        Cmd.__init__(self)

    def setupprompt(self):
        """ Change the prompt to show current frame, bowler, and ball """
        self.prompt = "%s: Frame #%s, Ball #%s> " % (self.game.bowler, self.game.frame+1, self.game.ball+1)

    def emptyline(self):
        """ check for emtpy line; set pins to 0 """
        self.game.talleyPins(0)
    
    def default(self, line):
        """ check line input """
        if line.lower() in ['p','s','score']:
            print self.game.getScores()
            return
        
        if line.lower() in ['q','e','quit','exit']:
            return True
        
        if not line.isdigit():
            print "ERROR: invalid pin value"
            return
        
        pins = int(line)
        if pins > 10 or pins < 0:
            print "ERROR: invalid pin value"
            return
        
        try:
            self.game.talleyPins(pins)
        except ValueError:
            print "ERROR: Invalid pin value!"

    def postcmd(self, stop, line):
        """ actions to perform after loop """
        self.setupprompt()
        return stop or self.game.finished

    

def main():
    opts = Opts()
    if not opts.player:
        print "ERROR: no players entered"
        return 1
    
    players = [Player(i) for i in opts.player]
    game = Game(players, opts.frames)
    GameLoop(game).cmdloop()

    print "\n\nFinal Score:\n"
    print game.getScores()


if __name__ == "__main__":
    sys.exit(main())
