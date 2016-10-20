from zipline.api import *

def universe():
    return [ "SPY" ]

def initialize(context):
    context.sid = symbol("SPY") #spy

    schedule_function(rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open())

def rebalance(context, data):
    price_history = data.history(context.sid, 'price', 200, '1d')

    if data.current(context.sid, "close") > price_history.mean():
        order_target_percent(context.sid, 1)
    else:
        order_target_percent(context.sid, 0)


def handle_data(context, data):
    pass
