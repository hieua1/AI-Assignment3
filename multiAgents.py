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

ooNum = 1000000

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
        minGhostDis = 1000000
        minFoodDis = 1000000
        xxx = 0
        curFood = currentGameState.getFood()
        for x, y in curFood.asList():
          if abs(x-newPos[0])+abs(y-newPos[1])<minFoodDis:
            minFoodDis = abs(x-newPos[0])+abs(y-newPos[1])
        for ghostState in newGhostStates:
          x, y = ghostState.getPosition()
          if abs(x-newPos[0])+abs(y-newPos[1])<=1:
            xxx = ooNum
        return -minFoodDis-xxx

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
    def bounded_minimax(self, curGameState, remainDepth, numAgents):
      agentId = remainDepth%numAgents
      if agentId!=0:
        agentId = numAgents - agentId
      legalMoves = curGameState.getLegalActions(agentId)
      if remainDepth==0 or len(legalMoves)==0:
        return (self.evaluationFunction(curGameState),'')
      "random.choice([Directions.NORTH,Directions.SOUTH,Directions.WEST,Directions.EAST,Directions.STOP]"
      legalSuccessor = [curGameState.generateSuccessor(agentId, action) for action in legalMoves]
      scoredArr = [self.bounded_minimax(successorGameState, remainDepth-1, numAgents)[0] for successorGameState in legalSuccessor]
      if agentId==0:
        bestScore=max(scoredArr)
      else:
        bestScore=min(scoredArr)
      bestIndices = [index for index in range(len(scoredArr)) if scoredArr[index]==bestScore]
      chosenIndex = random.choice(bestIndices)
      return (bestScore, legalMoves[chosenIndex])
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
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        return self.bounded_minimax(gameState, self.depth*numAgents, numAgents)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alpha_beta_pruning(self, curGameState, remainDepth, numAgents, alpha, beta):
      agentId = remainDepth%numAgents
      if agentId!=0:
        agentId = numAgents - agentId
      legalMoves = curGameState.getLegalActions(agentId)
      if remainDepth==0 or len(legalMoves)==0:
        return (self.evaluationFunction(curGameState),'')
      "random.choice([Directions.NORTH,Directions.SOUTH,Directions.WEST,Directions.EAST,Directions.STOP]"
      scoredArr = []
      if agentId==0:
        lowerBound = -ooNum
        for action in legalMoves:
          successorGameState = curGameState.generateSuccessor(agentId, action)
          v = self.alpha_beta_pruning(successorGameState, remainDepth-1, numAgents,alpha, beta)[0]
          scoredArr.append(v)
          lowerBound = max(lowerBound, v)
          if lowerBound>beta:
            return (lowerBound,'')
          alpha = max(alpha, v)
        bestScore = lowerBound
      else:
        upperBound = ooNum
        for action in legalMoves:
          successorGameState = curGameState.generateSuccessor(agentId, action)
          v = self.alpha_beta_pruning(successorGameState, remainDepth-1, numAgents,alpha, beta)[0]
          scoredArr.append(v)
          upperBound = min(upperBound, v)
          if upperBound<alpha:
            return (upperBound,'')
          beta = min(beta, v)
        bestScore = upperBound
      bestIndices = [index for index in range(len(scoredArr)) if scoredArr[index]==bestScore]
      chosenIndex = random.choice(bestIndices)
      return (bestScore, legalMoves[chosenIndex])

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        return self.alpha_beta_pruning(gameState, self.depth*numAgents, numAgents, -ooNum, ooNum)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, curGameState, remainDepth, numAgents):
      agentId = remainDepth%numAgents
      if agentId!=0:
        agentId = numAgents - agentId
      legalMoves = curGameState.getLegalActions(agentId)
      if remainDepth==0 or len(legalMoves)==0:
        return (self.evaluationFunction(curGameState),'')
      "random.choice([Directions.NORTH,Directions.SOUTH,Directions.WEST,Directions.EAST,Directions.STOP]"
      legalSuccessor = [curGameState.generateSuccessor(agentId, action) for action in legalMoves]
      scoredArr = [self.expectimax(successorGameState, remainDepth-1, numAgents)[0] for successorGameState in legalSuccessor]
      if agentId==0:
        bestScore=max(scoredArr)
        bestIndices = [index for index in range(len(scoredArr)) if scoredArr[index]==bestScore]
        chosenIndex = random.choice(bestIndices)
      else:
        bestScore=sum(i for i in scoredArr)
        chosenIndex = 0
        
      return (bestScore, legalMoves[chosenIndex])

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        return self.expectimax(gameState, self.depth*numAgents, numAgents)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    curFood = currentGameState.getFood()
    curPos = currentGameState.getPacmanPosition()
    ghostStatesList = currentGameState.getGhostStates()
    capsulesList = currentGameState.getCapsules()
    minScaredGhostDis = ooNum
    minActiveGhostDis = ooNum
    minFoodDis = ooNum
    minCapsulesDis = ooNum
    numCapsules = len(capsulesList)
    numFoods = len(curFood.asList())
    if (numFoods==0):
      minFoodDis = 0
    if numCapsules==0:
      minCapsulesDis = 0

    xxx = 0
    for x, y in curFood.asList():
      if abs(x-curPos[0])+abs(y-curPos[1])<minFoodDis:
        minFoodDis = abs(x-curPos[0])+abs(y-curPos[1])

    scaredGhosts, activeGhosts = [], []
    for ghost in currentGameState.getGhostStates():
      if not ghost.scaredTimer:
        activeGhosts.append(ghost)
      else: 
        scaredGhosts.append(ghost)
    if len(activeGhosts)==0:
      minActiveGhostDis = 0
    for ghostState in activeGhosts:
      x, y = ghostState.getPosition()
      if abs(x-curPos[0])+abs(y-curPos[1])<minActiveGhostDis:
        minActiveGhostDis = abs(x-curPos[0])+abs(y-curPos[1])
      if abs(x-curPos[0])+abs(y-curPos[1])<=1:
        xxx = ooNum
    if len(scaredGhosts)==0:
      minScaredGhostDis = 0
    for ghostState in scaredGhosts:
      x, y = ghostState.getPosition()
      if abs(x-curPos[0])+abs(y-curPos[1])<minScaredGhostDis and abs(x-curPos[0])+abs(y-curPos[1])<ghostState.scaredTimer:
        minScaredGhostDis = abs(x-curPos[0])+abs(y-curPos[1])

    for x, y in capsulesList:
      if abs(x-curPos[0])+abs(y-curPos[1])<minCapsulesDis:
        minCapsulesDis = abs(x-curPos[0])+abs(y-curPos[1])
    
    if minActiveGhostDis>3:
      minActiveGhostDis = 0
    return currentGameState.getScore()/3 - numCapsules*70 - minScaredGhostDis*10 - numFoods*7 - minFoodDis - minCapsulesDis*5 - xxx
  
# Abbreviation
better = betterEvaluationFunction

