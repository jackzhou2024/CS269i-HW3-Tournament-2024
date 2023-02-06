# Iterated File-Sharing Dilemma

This is the CS 269i class project developed by Jinkun Geng. 


How this works:
You are required to write a bidding strategy, following the template in exampleStrats, i.e., you will implement a function called strategy

We will compete your strategy against some baselines, as shown in exampleStrats. We will run multiple times: 

During every time, your bot and the baseline will compete for 10000 rounds.
For every 10000 rounds, we use the same auction mode. There are three auction modes in our implementation (SINGLE_ITEM_FIRST_PRICE, SINGLE_ITEM_SECOND_PRICE,
SINGLE_ITEM_ALL_PAY). The auction mode will determine how to calculate the scores for bots. (please refer to calcScores function in game_run.py) 


During each round, both your bot and the baseline will be given an initial value independently chosen from [0,1]. At the beginning of round i, your are also provided with the history in the past i-1 rounds. (refer to the comments in exampleStrats/random_bid.py). The history might be helpful for you to derive the auction mode used in this 10000 rounds, so that you can better design your strategy. 




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