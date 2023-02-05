# Iterated File-Sharing Dilemma

This is the CS 269i class project developed by the former CS269i student, Cary Huang (We really appreciate for Cary's wonderful work).



Nicky Case's "The Evolution of Trust" is also super fascinating, but it's not necessary to understand this project: https://ncase.me/trust/

How this works:
When you run code/dilemma_run.py, it will search through all the Python strategy files in code/exampleStrats. Then, it will simulate "Iterated Prisoner's Dilemma" with every possible pairing. (There are (n choose 2) pairings.) After all simulations are done, it will average each strategies' overall score. It will then produce a leaderboard of strategies based on their average performance, and save it to results.txt.

If you'd like to add your own strategy, all you have to do is create a new .py file in the code/exampleStrats folder that follows the same format as the others. Then, when you run code/dilemma_run.py, it should automatically include your strategy into the tournament!

# Details
| Payout Chart  | Player A cooperates | Player A defects |
| ------------- | ------------- | ------------- |
| Player B cooperates  | A: +3, B: +3  | A: +5, B: +0  |
| Player B defects  | A: +0, B: +5  | A: +1, B: +1  |

In this code, 0 = 'D' = defecting, and 1 = 'C' = cooperating.

---

Strategy functions take in two parameters, 'history' and 'memory', and output two values: 'moveChoice' and 'memory'. 'history' is a 2\*n numpy array, where n is the number of turns so far. Axis one corresponds to "this player" vs "opponent player", and axis two corresponds to what turn number we're on.
For example, it might have the values
```
 [[0 0 1]       a.k.a.    D D C
  [1 1 1]]      a.k.a.    C C C
```
In this case, there have been 3 turns, we have defected twice then cooperated once, and our opponent has cooperated all three times.

'memory' is a very open-ended parameter that can takes on any information that should be retained, turn-to-turn. Strategies that don't need memory, like Tit-for-tat, can simply return None for this variable. If you want to keep track of being 'wronged', like grimTrigger.py, you can set memory to True or False. If you have an extremely complicated strategy, you have make 'memory' store a list of arbitrarily many varibles!

For the outputs: the first value is just the move your strategy chooses to make, with 0 being defect and 1 being cooperate. The second value is any memory you'd like to retain into the next iteration. This can be 'None'.

---

Each pairing simulation runs for this many turns:
```
200-40*np.log(random.random())
```
This means each game is guaranteed to be at least 200 turns long. But then, for every turn after the 200th, there is an equal probability that the game ends. The probability is very low, so there should be no strategizing to defect on the very last turn consequence-free.


# Tasks
You are expected to write a python file named strategy.py (Please keep this name!). In this file you are expected to implement a function named strategy. After you finish you code, put the strategy.py to the folder exampleStrats, run the dilemma_run.py.

# Tips

To start from a clean Python enviornment, I suggest you use conda 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

First, install conda

Second, create a clean python enviornment (say python 3.7) with conda

Third, install any deps and execute your script in that conda enviornment 

The major commands are as below. 

```
conda create --name [NAME]

conda activate [NAME]

conda install pip

pip install -r requirements.txt
```

After you have successfully create the environment, enter the code environment, and run dilemma_run.py

```
cd code 

python dilemma_run.py
```

Without writing any code, you should be able to run the competition for the existing strategies in the exampleStrats folder. Then, you write your own strategy.py and put the file into the folder, rerun dilemma_run.py to see whether you can beat these baselines.


# Note

All you need to do is to write a strategy.py file and add it to exampleStrats. No need to change any existing files.

When submitting to gradescope, you only submit strategy.py, no other files are needed.

For any questions, feel free to make a post on edstem.