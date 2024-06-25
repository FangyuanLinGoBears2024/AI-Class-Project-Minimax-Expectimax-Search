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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"
        ghostCost = 0
        foodReward = 0
        newFoodList = newFood.asList()
        newGhostPos = [gs.getPosition() for gs in newGhostStates]
        if currentGameState.hasFood(newPos[0], newPos[1]):
            foodReward += 10
        if len(newFoodList) > 0:
            closestFoodDistance = min([manhattanDistance(newPos, f) for f in newFoodList])
            foodReward += 1/(1+closestFoodDistance)
        for i in range(len(newGhostPos)):
            if manhattanDistance(newPos, newGhostPos[i]) <= 4:
                if newScaredTimes[i] > 0:
                    ghostCost -= 200
                else:
                    if manhattanDistance(newPos, newGhostPos[i]) <= 1:
                        ghostCost += 10000
                    else:
                        ghostCost += 500         
        totalScaredTime = sum(newScaredTimes)
        return -ghostCost + foodReward + totalScaredTime

def scoreEvaluationFunction(currentGameState: GameState):
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
    

    def getAction(self, gameState: GameState):
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
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, d):
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            v = float('-inf')
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                v2, action2 = minValue(gameState.generateSuccessor(0, action), 1, d)
                if v2 > v:
                    v, move = v2, action
            return (v, move)
        def minValue(gameState, agentIndex, d):
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            v = float('inf')
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    v2, action2 = maxValue(gameState.generateSuccessor(agentIndex, action), d + 1)
                else: 
                    v2, action2 = minValue(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, d)
                if v2 < v:
                    v, move = v2, action
            return (v, move)
        value, move = maxValue(gameState, 0)
        return move

    
        
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, lower, upper, d):
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            v = float('-inf')
            move = None
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                v2, action2 = minValue(gameState.generateSuccessor(0, action), 1, lower, upper, d)
                if v2 > v:
                    v, move = v2, action
                    lower = max(v, lower)
                if v > upper:
                    return v, move
            return (v, move)
        def minValue(gameState, agentIndex, lower, upper, d):
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            v = float('inf')
            move = None
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    v2, action2 = maxValue(gameState.generateSuccessor(agentIndex, action), lower, upper, d + 1)
                else: 
                    v2, action2 = minValue(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, lower, upper, d)
                if v2 < v:
                    v, move = v2, action
                    upper = min(v, upper)
                if v < lower:
                    return v, move
            return (v, move)
        value, move = maxValue(gameState, float('-inf'), float('inf'), 0)
        return move
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, lower, upper, d):
            if gameState.isWin() or gameState.isLose() or d == self.depth:
                return (self.evaluationFunction(gameState), None)
            v = float('-inf')
            move = None
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                v2, action2 = expectValue(gameState.generateSuccessor(0, action), 1, lower, upper, d)
                if v2 > v:
                    v, move = v2, action
                    lower = max(v, lower)
                if v > upper:
                    return v, move
            return (v, move)
        def expectValue(gameState, agentIndex, lower, upper, d):
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            v = 0
            move = None
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    v2, action2 = maxValue(gameState.generateSuccessor(agentIndex, action), lower, upper, d + 1)
                else: 
                    v2, action2 = expectValue(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, lower, upper, d)
                v += v2
            return (v/len(legalActions), move)

        value, move = maxValue(gameState, float('-inf'), float('inf'), 0)
        return move

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    If win, then the state has infinite score. If the state is a lose, then it has negative infinite score.
    The number of foods left and the distance to the closest food negatively corresponds to the score.
    When ghosts are scared, getting close to them gains score. Otherwise we do the opposite.
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    ghostCost = 0
    foodReward = 0
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    foodList = food.asList()
    ghostPos = [gs.getPosition() for gs in ghostStates]
    foodReward -= 10 * len(foodList)
    if len(foodList) > 0:
        closestFoodDistance = min([manhattanDistance(pos, f) for f in foodList])
        foodReward += 10 * 1/(1+closestFoodDistance)
    for i in range(len(ghostPos)):
        if scaredTimes[i] > 0:
                ghostCost -= 200 * 1/(1+manhattanDistance(pos, ghostPos[i]))
        else:
            if manhattanDistance(pos, ghostPos[i]) <= 4:
                if manhattanDistance(pos, ghostPos[i]) <= 1:
                    ghostCost += 10000
                else:
                    ghostCost += 500         
    totalScaredTime = sum(scaredTimes)
    return -ghostCost + foodReward + totalScaredTime
    

# Abbreviation
better = betterEvaluationFunction
