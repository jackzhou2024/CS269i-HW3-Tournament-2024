# Auction Auto-bidding Tournament

This tournament code was originally developed by Jinkun Geng and modified by Jack Zhou for the value-maximizing setting.


How this works:
Your task is to write a bidding strategy, following the template in exampleStrats; i.e., you will implement a function called strategy. We will run your strategy in a 10,000-round-repeated auction against both baseline auto-bidders (as shown in exampleStrats), and classmates' auto-bidders. We'll first explain the auction formats and objective of value maximization, and then describe how scores are calculated and the task in more detail. You'll find some tips at the very bottom. Good luck!

1) _Auction formats._ In practice, ad auctions are often very complicated and frequently change for both engineering and economic reasons. This makes it hard to legally commit to a specific auction format. Accordingly, we are not specifying the auction format a-priori (see restrictions on auction format below). Your auto-bidder will have to learn how to bid based on feedback (value, bid, payment, and allocation) from previous rounds.

There are three example auction modes in the code (e.g., singleItemFirstPrice, singleItemSecondPrice,
singleItemAllPay), but your auto-bidder should be robust to other auctions as well. The auction mode will determine how to calculate the allocation and payments for auto-bidders. During the gradescope competition, we might add more auction modes.

2) _Value maximization._ In practice, advertisers don't just have utility functions. They often have fixed budgets, which they don't mind fully spending. The **value** for an advertiser is their utility minus their budget spent. **Each bidder starts with a budget of 2,500 and must adhere to this total spending limit over the course of 10,000 rounds. The goal is to obtain as much total value as possible. Please note the goal here is value maximization, distinct from utility maximization.**

During each round, both your bidding strategy and your competitor's will be given an value independently chosen from a uniform distribution over [0,1]. At the beginning of round i, your are also provided with the history in the past i-1 rounds (refer to the comments in example strategies). The history might be helpful for you to derive the auction mode used in this 10000 rounds, so that you can better design your strategy. 

Regardless of the auction mode, you can assume that the payment is never more than your bid.

**Note:** Please do not write code that inspects or manipulates the auction format, the objective, or your opponents' strategies.


# Score Calculation
Your score is your total **value** across 10000 rounds of the auction.
You can refer to calcScore function in game_run.py for the methods of score calculation.

For example, say $v_W$, $v_L$ are values of winner/loser in the current round, $b_W$, $b_L$ are remaining bids , $B_W$, $B_L$ are remaining budgets, $s_W$, $s_L$ are total scores.
Then:


(1) SINGLE_ITEM_FIRST_PRICE, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$B_W$ -= $b_W$,
$B_L$ -= $0$.

(2) SINGLE_ITEM_SECOND_PRICE, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$B_W$ -= $b_L$,
$B_L$ -= $0$.

(3) SINGLE_ITEM_ALL_PAY, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$B_W$ -= $b_W$,
$B_L$ -= $b_L$.

You can check the auctionStrats folder to see how we implement these three modes to decide the allocation result (i.e., who is the winner) and the payment.

In our gradescope test, we may include new auction modes.


# Tasks
You are expected to write a python file named strategy.py (Please keep this name!). In this file you are expected to implement a function named strategy. After you finish you code, put the strategy.py to the folder exampleStrats, run the game_run.py.

Intuitively, you don't want to spend your budget too slowly or too quickly. We have made three example strategies which aim to pace the budget evenly across all rounds. 
- Bid shading: This strategy uses a gradient-based method to maintain a shading factor $\mu$, suppose the current value is $v$, the strategy bids $v / (\mu + 1)$. $\mu$ increases when spending is too fast, and decreases when spending is too slow.
- Throttling: This strategy uses a gradient-based method to maintain a throttling factor $\tau$, suppose the current value is $v$, the strategy bids $v$ with probability $\tau$ and bids $0$ with probability $1-\tau$. $\tau$ increases when spending is too fast, and decreases when spending is too slow.
- Reserve pricing:  This strategy uses a gradient-based method to maintain a reserve price $r$, suppose the current value is $v$, the strategy bids $v$ when $v > r$ and bids $0$ when  $1-v \le r$. $r$ decreases when spending is too fast, and increases when spending is too slow.


While designing your strategy function, you will receive your remaining budget, number remaining rounds, and the auction history of past rounds. You can choose to use/not use provided information to help you design better algorithms.

The example strategies include implementations of Multi-Arm Bandit (MAB) algoirthms, which are go-to algorithms for optimizing in an uncertain and dynamic environment. If you want to implement more MAB algorithms, you can use the MABWiser library to implement them, and we will install this library in our testing enviroment. You can read more info at https://fidelity.github.io/mabwiser/about.html and implement your MAB algorithm.


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

After you have successfully create the environment, enter the code environment, and run game_run.py

```
cd code 

python game_run.py
```

Without writing any code, you should be able to run the competition for the existing strategies in the exampleStrats folder. Then, you write your own strategy.py and put the file into the folder, rerun game_run.py to see whether you can beat these baselines.


# Note

All you need to do is to write a strategy.py file and add it to exampleStrats. No need to change any existing files.

When submitting to gradescope, you only submit strategy.py, no other files are needed.

For any questions, feel free to make a post on edstem.
