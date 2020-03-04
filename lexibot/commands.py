# coding=utf-8
from pathlib import Path
from clldutils.clilib import command, ParserError

from lexibot import Lexibot, list_datadirs

# from cldfbench.cli_util import with_datasets, add_catalog_spec
# from pylexibank.cli_util import add_dataset_spec

@command(name='list', usage="list the datasets")
def list(args):
    for d in list_datadirs(args.dirname):
        print(d.stem)


@command(name='run', usage="runs the update")
def run(args):
    for d in list_datadirs(args.dirname):
        bot = Lexibot(d)
        print("Checking %s" % bot.id)
        bot.run()
