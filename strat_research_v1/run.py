#!/usr/bin/env python

import click # http://click.pocoo.org/5/
import os, sys, runpy
import logbook
import hashlib
import records
import json
import pickle
import pyfolio as pf

from pathlib import Path
from importlib import import_module

from zipline.utils.factory import load_from_yahoo
from zipline.utils.factory import create_simulation_parameters

from zipline.algorithm import TradingAlgorithm

from zipline.utils.cli import Date, Timestamp

logbook.NestedSetup([
    logbook.NullHandler(level=logbook.DEBUG),
    logbook.StreamHandler(sys.stdout, level=logbook.INFO),
    logbook.StreamHandler(sys.stderr, level=logbook.ERROR),
]).push_application()

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

"""
Basically a reimplementation of the following but with my own goals:
/Users/jcurzon/anaconda/envs/zipline/lib/python3.4/site-packages/zipline/utils/run_algo.py
"""

@click.command()
@click.argument('file')
@click.option(
    '-s',
    '--start',
    type=Date(tz='utc', as_timestamp=True),
    required=True,
    help='The start date of the simulation.',
)
@click.option(
    '-e',
    '--end',
    type=Date(tz='utc', as_timestamp=True),
    required=True,
    help='The end date of the simulation.',
)
def main(start, end, file):
    """Runs a strategy in FILE and saves the data in the database"""
    path = Path(file)

    if not path.is_file() or not os.access(file, os.R_OK):
        print ("File is missing")
        sys.exit(2)

    result = runpy.run_path(file, None, file)

    data = load_from_yahoo(stocks=result.get('universe')(), indexes={}, start=start, end=end)
    data = data.dropna()

    algo = TradingAlgorithm(
        handle_data=result.get('handle_data'),
        initialize=result.get('initialize'),
        before_trading_start=result.get('before_trading_start'),
        sim_params=create_simulation_parameters(
            start=start,
            end=end,
            data_frequency='daily',
        ),
    )

    perf = algo.run(data)
    dir(perf)
    write_to_db(file, perf, start= start, end=end)

def render_pyfolio(perf):
    returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_zipline(results)

    pf.create_full_tear_sheet(returns, positions=positions,
                              transactions=transactions, gross_lev=gross_lev, round_trips=True)

def write_to_db(file, perf, **kwargs):
    with open(file, "rb") as f:
        b_contents = f.read()

    digest = hashlib.md5(b_contents).hexdigest()

    db = records.Database(config['database']['url'])
    db.query("""
        insert into strategies (filepath, body, md5sum)
        values (:path, :body, :checksum)
        on conflict do nothing
        """,
        path=file, body=b_contents.decode("utf-8"), checksum=digest)

    result = db.query("""
        insert into test_runs
        (strategy_id, parameters, results, pickle, created_at, starts_at, ends_at)
        values (
            (select id from strategies where md5sum = :strategy_checksum),
            :parameters, :results, :pickle_data, now(), :starts_at, :ends_at
        ) returning id
        """,
        strategy_checksum= digest,
        parameters= json.dumps({}),
        results= json.dumps({}),
        pickle_data= pickle.dumps(perf),
        starts_at= kwargs.pop('start'),
        ends_at= kwargs.pop('end'),
    )

    run_id = result.all()[0].id
    print("Test run saved as {run_id}".format(run_id=run_id))


if __name__ == '__main__':
    main()
