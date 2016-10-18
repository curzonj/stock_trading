#!/usr/bin/env python

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import click # http://click.pocoo.org/5/
import records
import json
import pickle
import pyfolio as pf
import matplotlib.pyplot as plt

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

@click.command()
@click.argument('run_id')
def main(run_id):
    db = records.Database(config['database']['url'])
    rows = db.query("select * from test_runs where id = :id", id=run_id)
    results = pickle.loads(rows[0].pickle)

    returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_zipline(results)

    # pulled from /Users/jcurzon/anaconda/envs/zipline/lib/python3.4/site-packages/pyfolio
    benchmark_rets = pf.utils.get_symbol_rets('SPY')

    # If the strategy's history is longer than the benchmark's, limit strategy
    if returns.index[0] < benchmark_rets.index[0]:
        returns = returns[returns.index > benchmark_rets.index[0]]

    pf.create_returns_tear_sheet(
        returns,
        live_start_date=None,
        cone_std=(1.0, 1.5, 2.0),
        benchmark_rets=benchmark_rets,
        set_context=True)

    plt.savefig("returns_{run_id}.png".format(run_id=run_id))

if __name__ == '__main__':
    main()
