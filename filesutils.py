"""Module intended to process all io operations related to operating
system"""
import os
import csv
import json
from config import INDIR, OUTDIR
import argparse
from inspect import currentframe, getframeinfo
from modes import MODES
import random

# GENERATORS


def produce_fileslit_recur(root_dir):
    fileslist = []
    for _r, _d, _f in os.walk(root_dir):
        for f in _f:
            fileslist.append(os.path.join(_r, f))
    return fileslist


# OUT FILES


def list_to_csv(target_path, data):
    if not data:
        raise Exception(f"data for {target_path} corrupted")

    if isinstance(data, list):
        data.sort(key = lambda _ : _[0])
    else:
        data.sort(key = lambda _ : _)

    with open(target_path, "w") as outfile:
        writer = csv.writer(outfile)
        for line in data:
            if isinstance(line, list):
                writer.writerow(line)
            else:
                writer.writerow([line])

def dict_to_json(target_path, data):
    with open(target_path, "w") as outfile:
        json.dump(data, outfile, indent=2)


# IN FILES


def csv_to_list(target_path):
    with open(target_path, "r") as infile:
        reader = csv.reader(infile)
        return list(_ if len(_) > 1 else _[0] for _ in reader)


def json_to_dict(target_path):
    with open(target_path, "r") as infile:
        return json.load(infile)


# HIGH LEVEL IO


def prepare_arg_parser():

    parser = argparse.ArgumentParser(
        description="Arg structure v1 mode type action did",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-m", "--mode", help="[two(classes), sort, ...]")
    parser.add_argument("-s", "--submode", help="[template, ...]")
    parser.add_argument("-t", "--data_type", help="[files(list), ...]")
    parser.add_argument("-a", "--action", help="gen|in")
    parser.add_argument("-d", "--dataid", help="data identifier str")
    parser.add_argument("-b", "--batch", help="n")
    return parser


def read_input(target_id, batch_size = None):
    """json of structure + csv of data"""
    outfile_prev = os.path.join(INDIR, target_id)

    csv_in = outfile_prev + ".csv"
    data_list = csv_to_list(csv_in)
    data_extracted = data_list[::]

    if batch_size:
        data_extracted = random.sample(data_list, min(10, len(data_list)))

    prev_data = list(_ for _ in data_list  if _ not in data_extracted)
        
    if prev_data:
        list_to_csv(csv_in, prev_data)

    json_in = outfile_prev + ".json"
    data_json = json_to_dict(json_in)
    data_json["payload"] = data_extracted

    return data_json


def write_output(prefix, target_id, processed_data):
    """id -> one <...>.csv for each processed list"""
    outfile_prev = OUTDIR
    target_file = os.path.join(outfile_prev, prefix+target_id)
    target_file += ".csv"
    list_to_csv(target_file, processed_data)


def generate_data(dataid, datatype):
    if datatype == "files":
        outfile_prev = os.path.join(INDIR, os.path.basename(dataid))

        fileslist = produce_fileslit_recur(dataid)
        csv_out = outfile_prev + ".csv"
        list_to_csv(csv_out, fileslist)

        json_out = outfile_prev + ".json"
        json_data = {"datatype": datatype, "meta": dataid, "modes": {}}
        for mode in MODES:
            json_data["modes"][mode] = {"template": ["lower", "higher"]}
        # /mnt/X/ARCH_META/Pictures
        dict_to_json(json_out, json_data)
    elif datatype == "text":
        outfile_prev = os.path.join(INDIR, os.path.basename(dataid))

        entities_list = []
        with open(dataid) as source_file:
            for line in source_file:
                entities_list.append(line)

        csv_out = outfile_prev + ".csv"
        list_to_csv(csv_out, entities_list)

        json_out = outfile_prev + ".json"
        json_data = {"datatype": datatype, "meta": dataid, "modes": {}}
        for mode in MODES:
            json_data["modes"][mode] = {"template": ["lower", "higher"]}
        dict_to_json(json_out, json_data)
        datafile = datatype
    else:
        raise (NotImplementedError)


def resolve_cli_arg(cli_args):
    """convert input to sane dictionary 'bout IN -> OUT schema"""
    if not "dataid" in cli_args or not "data_type" in cli_args:
        raise (
            f"Well, well fuck, I mean, I just don't know what to say. {__file__}:{getframeinfo(currentframe()).lineno}"
        )

    print(cli_args)
    print()
    if cli_args.action == "gen":
        generate_data(cli_args.dataid, cli_args.data_type)
        return "DONE"
    elif cli_args.action == "in":
        if not "mode" in cli_args or not "submode" in cli_args:
            raise (
                f"Well, well fuck, I mean, I just don't know what to say. {__file__}:{getframeinfo(currentframe()).lineno}"
            )

        return read_input(cli_args.dataid, cli_args.batch)
    else:
        print(cli_args)
        raise (NotImplementedError)
