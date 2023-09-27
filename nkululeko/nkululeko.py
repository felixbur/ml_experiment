# nkululeko.py
# Entry script to do a Nkululeko experiment

import os.path
import configparser
import argparse
import nkululeko.experiment as exp
from nkululeko.util import Util
from nkululeko.constants import VERSION


def main(src_dir):
    parser = argparse.ArgumentParser(
        description="Call the nkululeko framework."
    )
    parser.add_argument(
        "--config", default="exp.ini", help="The base configuration"
    )
    args = parser.parse_args()
    if args.config is not None:
        config_file = args.config
    else:
        config_file = f"{src_dir}/exp.ini"

    # test if the configuration file exists
    if not os.path.isfile(config_file):
        print(f"ERROR: no such file: {config_file}")
        exit()

    # load one configuration per experiment
    config = configparser.ConfigParser()
    config.read(config_file)

    # create a new experiment
    expr = exp.Experiment(config)
    util = Util("nkululeko")
    util.debug(
        f"running {expr.name} from config {config_file}, nkululeko version"
        f" {VERSION}"
    )

    if util.config_val("EXP", "no_warnings", False):
        import warnings

        warnings.filterwarnings("ignore")

    # load the data
    expr.load_datasets()

    # split into train and test
    expr.fill_train_and_tests()
    util.debug(
        f"train shape : {expr.df_train.shape}, test shape:{expr.df_test.shape}"
    )

    # extract features
    expr.extract_feats()

    # initialize a run manager
    expr.init_runmanager()

    # run the experiment
    expr.run()

    expr.store_report()

    print("DONE")


if __name__ == "__main__":
    cwd = os.path.dirname(os.path.abspath(__file__))
    main(
        cwd
    )  # use this if you want to state the config file path on command line
