from zipline.api import *

def initialize(context, **kwargs):
    context.sid = symbol(kwargs.pop('securities')[0]) #spy

def handle_data(context, data):
    order_target_percent(context.sid, 1)
