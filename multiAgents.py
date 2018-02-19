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
        v = ("unknown", float("inf"))
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
        v = ("unknown", float("-inf"))
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
        curDepth = 0
        currentAgentIndex = 0
        alpha = float("-inf")
        beta = float("inf")
        val = self.getValue(gameState, currentAgentIndex, curDepth, alpha, beta)
        return val[0] 

    def getValue(self, gameState, currentAgentIndex, curDepth, alpha, beta): 
        if currentAgentIndex >= gameState.getNumAgents():
            currentAgentIndex = 0
            curDepth += 1
        if curDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if currentAgentIndex == self.index:
            return self.getMaxValue(gameState, currentAgentIndex, curDepth, alpha, beta)
        else:
            return self.getMinValue(gameState, currentAgentIndex, curDepth, alpha, beta)
        
    def getMinValue(self, gameState, currentAgentIndex, curDepth, alpha, beta):
        v = ("unknown", float("inf"))
        if gameState.getLegalActions(currentAgentIndex):
            for x in gameState.getLegalActions(currentAgentIndex):
                if x != "Stop":
                    toReturn = self.getValue(gameState.generateSuccessor(currentAgentIndex, x), currentAgentIndex + 1, curDepth, alpha, beta)
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


    def getMaxValue(self, gameState, currentAgentIndex, curDepth, alpha, beta):
        v = ("unknown", float("-inf"))
        
        if gameState.getLegalActions(currentAgentIndex):
            for action in gameState.getLegalActions(currentAgentIndex):
                if action != "Stop":
                    toReturn = self.getValue(gameState.generateSuccessor(currentAgentIndex, action), currentAgentIndex + 1, curDepth, alpha, beta)
                    if type(toReturn) is tuple:
                        toReturn = toReturn[1] 
                    vNew = max(v[1], toReturn)
                    if vNew is not v[1]:
                        v = (action, vNew) 
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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
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

# Abbreviation
better = betterEvaluationFunction
