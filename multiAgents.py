# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print(newPos)
        # print(newFood.asList())
        # print(newGhostStates)
        # print(newScaredTimes)
        # print(successorGameState.getScore())
        "*** YOUR CODE HERE ***"

        foodDist = -1
        for food in newFood.asList():
            if foodDist < 0:
                foodDist = manhattanDistance(food, newPos)
            else:
                foodDist = min(manhattanDistance(food, newPos), foodDist)

        ghost_distances = []
        for ghost in newGhostStates:
            ghost_distances.append(manhattanDistance(newPos, ghost.getPosition()))

        total_food = 0
        for x in range(newPos[0]-2, newPos[0]+3):
            for y in range(newPos[1]-2, newPos[1]+3):
                if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
                    total_food += 1

        total1 = 100.0/foodDist + 100 * successorGameState.getScore()
        total2 = total1 + min(ghost_distances) if ghost_distances and min(ghost_distances) != 0 else total1 + 1
        total3 = total2 if len(newFood.asList()) == 0 else total2 + 100.0/len(newFood.asList())
        return total3 + 1 if total_food == 0 else total3 + total_food

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        currDepth = 0
        currIndex = 0
        val = self.value(gameState, currIndex, currDepth)
        return val[0]

    def value(self, gameState, currIndex, currDepth):
        if currIndex >= gameState.getNumAgents():
            currIndex = 0
            currDepth += 1
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)
        if currIndex == self.index:
            return self.getMaxValue(gameState, currIndex, currDepth)
        return self.getMinValue(gameState, currIndex, currDepth)

    def getMinValue(self, gameState, currIndex, currDepth):
        v = ("penis", float("inf"))
        if gameState.getLegalActions(currIndex):
            for x in gameState.getLegalActions(currIndex):
                if x != "Stop":
                    toReturn = self.value(gameState.generateSuccessor(currIndex, x), currIndex + 1, currDepth)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1]
                    minValue = min(v[1], toReturn)
                    if minValue is not v[1]:
                        v = (x, minValue)
            return v
        return self.evaluationFunction(gameState)

    def getMaxValue(self, gameState, currIndex, currDepth):
        v = ("penis", float("-inf"))
        if gameState.getLegalActions(currIndex):
            for x in gameState.getLegalActions(currIndex):
                if x != "Stop":
                    toReturn = self.value(gameState.generateSuccessor(currIndex, x), currIndex + 1, currDepth)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1]
                    maxValue = max(v[1], toReturn)
                    if maxValue is not v[1]:
                        v = (x, maxValue)
            return v
        return self.evaluationFunction(gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        currDepth = 0
        currIndex = 0
        alpha = float("-inf")
        beta = float("inf")
        val = self.getValue(gameState, currIndex, currDepth, alpha, beta)
        return val[0]

    def getValue(self, gameState, currIndex, currDepth, alpha, beta):
        if currIndex >= gameState.getNumAgents():
            currIndex = 0
            currDepth += 1
        if currDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if currIndex == self.index:
            return self.getMaxValue(gameState, currIndex, currDepth, alpha, beta)
        else:
            return self.getMinValue(gameState, currIndex, currDepth, alpha, beta)

    def getMinValue(self, gameState, currIndex, currDepth, alpha, beta):
        v = ("penis", float("inf"))
        if gameState.getLegalActions(currIndex):
            for x in gameState.getLegalActions(currIndex):
                if x != "Stop":
                    toReturn = self.getValue(gameState.generateSuccessor(currIndex, x), currIndex + 1, currDepth, alpha, beta)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1]
                    minValue = min(v[1], toReturn)
                    if minValue is not v[1]:
                        v = (x, minValue)
                    if v[1] < alpha:
                        return v
                    beta = min(beta, v[1])
            return v
        return self.evaluationFunction(gameState)


    def getMaxValue(self, gameState, currIndex, currDepth, alpha, beta):
        v = ("penis", float("-inf"))

        if gameState.getLegalActions(currIndex):
            for action in gameState.getLegalActions(currIndex):
                if action != "Stop":
                    toReturn = self.getValue(gameState.generateSuccessor(currIndex, action), currIndex + 1, currDepth, alpha, beta)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1]
                    maxValue = max(v[1], toReturn)
                    if maxValue is not v[1]:
                        v = (action, maxValue)
                    if v[1] > beta:
                        return v
                    alpha = max(alpha, v[1])
            return v
        return self.evaluationFunction(gameState)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        currDepth = 0
        currIndex = 0
        val = self.value(gameState, currIndex, currDepth)
        return val[0]

    def value(self, gameState, currIndex, currDepth):
        if currIndex >= gameState.getNumAgents():
            currIndex = 0
            currDepth += 1
        if currDepth == self.depth:
            return self.evaluationFunction(gameState)
        if currIndex == self.index:
            return self.getMaxValue(gameState, currIndex, currDepth)
        else:
            return self.getExpValue(gameState, currIndex, currDepth)

    def getExpValue(self, gameState, currIndex, currDepth):
        v = ["penis", 0]
        if gameState.getLegalActions(currIndex):
            for action in gameState.getLegalActions(currIndex):
                if action != "Stop":
                    toReturn = self.value(gameState.generateSuccessor(currIndex, action), currIndex + 1, currDepth)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1]
                    v[0] = action
                    v[1] += toReturn / len(gameState.getLegalActions(currIndex))
            return tuple(v)
        return self.evaluationFunction(gameState)


    def getMaxValue(self, gameState, currIndex, currDepth):
        v = ("penis", float("-inf"))

        if not gameState.getLegalActions(currIndex):
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(currIndex):
            if action != "Stop":
                toReturn = self.value(gameState.generateSuccessor(currIndex, action), currIndex + 1, currDepth)
                if type(toReturn) is tuple:
                    toReturn = toReturn[1]
                maxValue = max(v[1], toReturn)
                if maxValue is not v[1]:
                    v = (action, maxValue)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
        Factors to consider:
            - Food distance
            - Ghost distances
            - Leftover food
            - If a Ghost is Scared
            - The 'Special Dot'
            - Current Game Score

        Deduct from total 'weight' for remaining food dots and if a Ghost is NOT scared
        Each factor is scaled to a value that indicates its significance:
            - Game Score is most signifcant
            - The special dot is weighted more than others because of its effects on the ghosts
            - Food distances are the next most important value
            - Ghosts are split into 2 states:
                1. If the Ghost is normal (not scared), it has a negative value of 100/<Distance from Current Position>
                2. If the Ghost is scared, it is ok to be closer to a ghost (and they more points for being eaten)
            - Remaing Food is left as is

    """
    newPos = currentGameState.getPacmanPosition()
    newFood = [food for food in currentGameState.getFood().asList() if food]
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghost.scaredTimer for ghost in newGhostStates]

    # From OG EvaluationFunction
    foodDist = -1
    for food in newFood:
        if foodDist < 0:
            foodDist = manhattanDistance(food, newPos)
        else:
            foodDist = min(manhattanDistance(food, newPos), foodDist)

    ghostDist = []
    for ghost in newGhostStates:
        ghostDist.append(manhattanDistance(newPos, ghost.getPosition()))

    # New Features
    remainingFood = len(newFood)                               # We don't want remaining Food (less is better)
    scaredTime = min(newScaredTimes)                           # Minimize the 'danger' level of a ghost (smaller the number, more dangerous a ghost becomes)
    if scaredTime == 0:
        ghostDistScore = -100 / (min(ghostDist) + 1)           # Ghost is most dangerous since they are not scared
    else:
        ghostDistScore = 50 / (min(ghostDist) + 1) * 0.5       # Ghost is not as dangerous because they are scared

    foodDist = 60 / (foodDist + 1) if foodDist > 0 else 60     # Minimum food distances (scaled by weight)
    specialDot = scaredTime                                    # Scaling the special dot because it impacts the scared times
    gameScore = currentGameState.getScore()                    # Current game score is very important

    return (gameScore * 100) - remainingFood + (specialDot * 80) + foodDist + ghostDistScore

# Abbreviation
better = betterEvaluationFunction
