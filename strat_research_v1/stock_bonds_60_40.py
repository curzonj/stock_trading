from zipline.api import *

def universe():
    return [ "SPY", "LQD" ]

def initialize(context):
    schedule_function(rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open())

def rebalance(context, data):
    order_target_percent(symbol("SPY"), 0.6)
    order_target_percent(symbol("LQD"), 0.4)

def handle_data(context, data):
    pass
