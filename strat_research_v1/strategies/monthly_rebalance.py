from zipline.api import *

def universe():
    return [ "SPY", "LQD" ]

def initialize(context, **kwargs):
    context.symbols = [ symbol(a) for a in kwargs.pop('securities')]
    context.weights = [ float(a) for a in kwargs.pop('weights').split(',') ]

    schedule_function(rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open())

def rebalance(context, data):
    for idx, symbol in enumerate(context.symbols):
        order_target_percent(symbol, context.weights[idx])

def handle_data(context, data):
    pass
