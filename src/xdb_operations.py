# the operations on xdb that accelerate the simulator run
import os
import subprocess
import xml
import xml.dom.minidom
import time
import math
import json

from find_best_conf import decode_configuration, encode_configuration_and_store
from evaluate_target_conf import get_performance_from_xml

# from xdb_operations import transfer_files_to_xdb, load_xdb, find_in_xdb

# load everything in the xdb
def load_xdb(xdb_dir):
    xdb = {}
    
    # check if xdb_dir exists
    if not os.path.exists(xdb_dir):
        raise FileNotFoundError(f"xDB directory {xdb_dir} does not exist.")
    
    # get the configuration files in xdb
    configurations = {}
    config_dir = os.path.join(xdb_dir, "configurations")
    if os.path.exists(config_dir):
        for filename in os.listdir(config_dir):
            if "xml" not in filename:  # only consider xml files
                continue
            conf_vec = decode_configuration(os.path.join(config_dir, filename))
            if conf_vec is not None:
                filename = filename.replace(".xml", "")  # remove the .xml extension
                configurations[filename] = conf_vec
            else:
                print(f"Warning: Failed to decode configuration from {filename}. Skipping this file.")
    else:
        print(f"No configurations found in {config_dir}.")
    
    current_conf_num = len(configurations)
    print(f"Loaded {current_conf_num} configurations from xDB.")
    xdb["configurations"] = configurations

    # get the workload files in xdb

    workloads = {}

    workloads_dir = os.path.join(xdb_dir, "workloads")
    if os.path.exists(workloads_dir):
        for filename in os.listdir(workloads_dir):
            if not "scenario" in filename:  # only consider workload files that contain "scenario"
                continue
            confname = filename.split("_")[0]
            workload_name = filename.split("_")[1]  # remove the .xml extension and get the workload name
            assert(confname in configurations), f"INCONSISTENT DATABASE: Configuration {confname} not found in xdb configurations, but in xdb workloads."
            if confname not in workloads:
                workloads[confname] = []
            if workload_name not in workloads[confname]:
                workloads[confname].append(workload_name)
    
    print(f"Loaded {len(workloads)} configurations with workloads from xDB.")

    # add workloads to xdb
    xdb["workloads"] = workloads

    # get all the warmup file names
    warmup_files = []
    warmup_dir = os.path.join(xdb_dir, "warmup")
    if os.path.exists(warmup_dir):
        for filename in os.listdir(warmup_dir):
            warmup_files.append(filename)
    else:
        print(f"No warmup files found in {warmup_dir}.")
    
    xdb["warmup_files"] = warmup_files
    print(f"Loaded {len(warmup_files)} warmup files from xDB.")

    return xdb

def copy_file(src, dst):
    """
    Copy a file from src to dst.
    If the destination directory does not exist, it will be created.
    """
    # create the destination directory if it does not exist
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    # copy the file
    try:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                fdst.write(fsrc.read())
        # print(f"Copied {src} to {dst}.")
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")

# transfer files in existing simulator runs into xdb
def transfer_files_to_xdb(xdb_dir, simulator_runs_dir):
    # check if xdb_dir exists, if not create it
    xdb = load_xdb(xdb_dir)  # load the existing xdb
    
    # transfer files in */configurations
    configurations_dir_src = os.path.join(simulator_runs_dir, "configurations")
    workloads_dir_src = os.path.join(simulator_runs_dir, "workloads")
    all_workload_files = os.listdir(workloads_dir_src) if os.path.exists(workloads_dir_src) else []
    existing_configurations = xdb["configurations"]
    existing_workloads = xdb["workloads"]
    print(f"Transferring files from {simulator_runs_dir} to xDB at {xdb_dir}.")
    for filename in os.listdir(configurations_dir_src):
        if "xml" not in filename:   
            continue
        print(f"Processing configuration file: {filename}")
        conf_vec = decode_configuration(os.path.join(configurations_dir_src, filename))
        if conf_vec is None:
            print(f"Warning: Failed to decode configuration from {filename}. Skipping this file.")
            continue
        # check if the configuration already exists in xdb
        # TODO optimize this
        existing_confname = None
        for existing_filename, existing_conf_vec in existing_configurations.items():
            if existing_conf_vec == conf_vec:
                existing_confname = existing_filename
                break
        # find all the workloads for this configuration file
        filename = filename.replace(".xml", "")  # remove the .xml extension
        new_workloads_to_filenames = {}
        for w in all_workload_files:
            if not "scenario" in w:
                continue
            if w.startswith(filename + "_"):
                workload_name = w.split("_")[1]
                new_workloads_to_filenames[workload_name] = w
        # if the configuration already exists, we need to check if the workloads are already in xdb
        if existing_confname is not None:
            print(f"Configuration {existing_confname} already exists in xdb.")
            # check if the workloads are already in xdb
            for workload_name, workload_filename in new_workloads_to_filenames.items():
                if workload_name not in existing_workloads[existing_confname]:
                    new_workload_name = workload_filename.split("_")
                    new_workload_name[0] = existing_confname  # replace the configuration name with the existing one
                    new_workload_filename = "_".join(new_workload_name)
                    # add the new workload to xdb
                    copy_file(os.path.join(workloads_dir_src, workload_filename), os.path.join(xdb_dir, "workloads", new_workload_filename))
        else:
            print(f"Configuration {filename} does not exist in xdb. Adding it.")
            config_num = len(existing_configurations)
            new_confname = f"{config_num}"
            # add the new configuration to xdb
            copy_file(os.path.join(configurations_dir_src, filename + ".xml"), os.path.join(xdb_dir, "configurations", new_confname + ".xml"))
            # add all workloads for the new configuration to xdb
            for workload_name, workload_filename in new_workloads_to_filenames.items():
                new_workload_name = workload_filename.split("_")
                new_workload_name[0] = new_confname
                new_workload_filename = "_".join(new_workload_name)
                # copy the workload file to xdb
                copy_file(os.path.join(workloads_dir_src, workload_filename), os.path.join(xdb_dir, "workloads", new_workload_filename))
                # add the new workload to xdb
                existing_configurations[new_confname] = conf_vec  # add the new configuration to xdb
    
    # finally, copy the warmup files if they do not exist
    existing_warmup_files = xdb["warmup_files"]
    warmup_dir_src = os.path.join(simulator_runs_dir, "warmup")
    if os.path.exists(warmup_dir_src):
        for filename in os.listdir(warmup_dir_src):
            if filename not in existing_warmup_files:
                # copy the warmup file to xdb
                copy_file(os.path.join(warmup_dir_src, filename), os.path.join(xdb_dir, "warmup", filename))

    else:
        print(f"No warmup files found in {warmup_dir_src}.")

    print(f"Files transferred to {xdb_dir}")


xdb_cached = None
xdb_dir_cached = None

# search whether a given configuration is already in the xdb, return its filename if found
def find_in_xdb(xdb_dir, configpath, workloadname):
    global xdb_cached, xdb_dir_cached
    if xdb_dir_cached == xdb_dir:
        xdb = xdb_cached
    else:
        xdb = load_xdb(xdb_dir)
        xdb_cached = xdb
        xdb_dir_cached = xdb_dir
    # check if the configuration exists in xdb
    conf_vec = decode_configuration(configpath)
    if conf_vec is None:
        raise ValueError(f"Failed to decode configuration from {configpath}.")
    
    existing_confname = None
    for filename, existing_conf_vec in xdb["configurations"].items():
        if existing_conf_vec == conf_vec:
            existing_confname = filename
            break
    if existing_confname is not None:
        print(f"Configuration found in xdb: {existing_confname}.")
        # check if the workload exists for this configuration
        if existing_confname in xdb["workloads"]:
            workloads = xdb["workloads"][existing_confname]
            if workloadname in workloads:
                # return the performance results 
                workload_filename = f"{existing_confname}_{workloadname}_scenario_1.xml"  # assuming scenario_1.xml is the default workload file
                workload_path = os.path.join(xdb_dir, "workloads", workload_filename)
                result = get_performance_from_xml(workload_path)
                if result is None:
                    cmd = "rm -f " + workload_path  # remove the file if no performance results found
                    subprocess.run(cmd, shell=True)
                    return None  # no performance results found
                else:
                    print(f"Performance results found for workload {workloadname} under configuration {existing_confname}.")
                    return result[0:5]  # return the performance results
            else:
                print(f"Workload {workloadname} not found for configuration {existing_confname}.")
        else:
            print(f"No workloads found for configuration {existing_confname}.")
    return None


