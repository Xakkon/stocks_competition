import pandas as pd
from decision import Decision

INITIAL_MONEY = 1000
INITIAL_STOCK = 0

class Balance:
    def __init__(self):
        self.money = INITIAL_MONEY
        self.stock = INITIAL_STOCK
    
    def __str__(self):
        return f"Balance({self.money}$, {self.stock} stocks)"


def simulate(old_df, new_df, verbose=False):
    def log(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    from strategy import act
    df = pd.concat([old_df, new_df], ignore_index=True)
    balance = Balance()
    print(f"Initial balance: {balance}")
    
    for row in df.itertuples():
        history_at_moment = df.loc[0:row.Index]
        log(f"{row.date.date()} | price is {row.price}$, balance: {balance}")

        decision = act(row, history_at_moment, balance)
        if decision is None:
            decision = Nothing()
        if not isinstance(decision, Decision):
            raise ValueError(f"act() must return either Decision object or None, not {type(decision)}")

        log(f"Decided to {decision}")

        error = decision.validate(row, decision, balance)
        if error is not None:
            log(f"Invalid decision: {error}")
            raise ValueError(f"Invalid decision: {error}")
        
        decision.apply(row, history_at_moment, balance)
    print(f"Final balance: {balance}")


if __name__ == "__main__":
    import argparse
    import os.path
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('old_data', type=str)
    parser.add_argument('new_data', type=str)
    parser.add_argument('--verbose', default=False, action='store_true')
    args = parser.parse_args() #argparse.Namespace(**{'old_data': 'data_old.csv', 'new_data': 'data_new.csv', 'verbose': True})

    if not os.path.isfile(args.old_data):
        print(f"File {args.old_data} not found")
        sys.exit(1)
    if not os.path.isfile(args.new_data):
        print(f"File {args.new_data} not found")
        sys.exit(1)
    
    old_df = pd.read_csv(args.old_data, parse_dates=["date"])
    new_df = pd.read_csv(args.new_data, parse_dates=["date"])
    verbose = args.verbose

    old_df = old_df.sort_values(by="date")
    new_df = new_df.sort_values(by="date")
    
    if any(new_df['date'] < old_df['date'].iloc[-1]):
        print(f"Dates in new data must not be older than in old data")
        sys.exit(1)

    simulate(old_df, new_df, verbose=verbose)
