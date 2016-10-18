from zipline.api import * 

def universe():
    return [ "SPY" ]

def initialize(context):
    context.sid = symbol("SPY") #spy

def handle_data(context, data):
    order_target_percent(context.sid, 1)
