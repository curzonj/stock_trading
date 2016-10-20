#!/usr/bin/env python

import click # http://click.pocoo.org/5/
import os, sys, runpy
import logbook
import hashlib
import records
import json
import pickle
import pyfolio as pf
import pandas as pd

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
@click.argument('algofile', type=click.File('r'))
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
@click.option('--save/--no-save', default=True)
@click.option('-D', '--define', multiple=True)
@click.option('--securities', required=True)
def main(algofile, start, end, save, define, securities):
    """Runs a strategy in FILE and saves the data in the database"""
    frequency = 'daily'

    symbols = [ a.upper() for a in securities.split(',') ]

    start_data = start - pd.DateOffset(months=12)

    define_parts = [ assign.split('=', 2) for assign in define ]
    define_dict = { a[0] : a[1] for a in define_parts }
    define_dict['securities'] = symbols
    define_dict['frequency'] = frequency

    data = load_from_yahoo(stocks=symbols, indexes={}, start=start_data, end=end)
    data = data.dropna()

    algotext = algofile.read()
    algoname = getattr(algofile, 'name', '<algorithm>')

    algo = TradingAlgorithm(
        script=algotext,
        algo_filename= algoname,
        sim_params=create_simulation_parameters(
            start=start,
            end=end,
            data_frequency=frequency
        ),
        **define_dict
    )

    perf = algo.run(data, overwrite_sim_params=False)
    if save:
        write_to_db(algoname, algotext, perf, define_dict, start, end)

def render_pyfolio(perf):
    returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_zipline(results)

    pf.create_full_tear_sheet(returns, positions=positions,
                              transactions=transactions, gross_lev=gross_lev, round_trips=True)

def write_to_db(name, algotext, perf, parameters, start, end):
    digest = hashlib.md5(algotext.encode("utf-8")).hexdigest()

    db = records.Database(config['database']['url'])
    db.query("""
        insert into strategies (name, body, md5sum)
        values (:name, :body, :checksum)
        on conflict do nothing
        """,
        name=name, body=algotext, checksum=digest)

    result = db.query("""
        insert into test_runs
        (strategy_id, securities, parameters, results, pickle, created_at, starts_at, ends_at)
        values (
            (select id from strategies where md5sum = :strategy_checksum),
            :securities, :parameters, :results, :pickle_data, now(), :starts_at, :ends_at
        ) returning id
        """,
        strategy_checksum= digest,
        securities= parameters['securities'],
        parameters= json.dumps(parameters),
        results= json.dumps({}),
        pickle_data= pickle.dumps(perf),
        starts_at= start,
        ends_at= end,
    )

    run_id = result.all()[0].id
    print("Test run saved as {run_id}".format(run_id=run_id))


if __name__ == '__main__':
    main()
