import os
import time
from evaluate_target_conf import generate_config_workload, save_to_xdb, get_performance_from_xml, evaluate_config_workload, generate_queuetest_config_workload

# proccesses in progress

if __name__ == "__main__":
    import sys

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    if len(sys.argv) != 3:
        print("Usage: batch_evaluation.py exp_name target_name")
        exit()
    exp_name = sys.argv[1]
    target_name = sys.argv[2]

    if exp_name == "Coarsed_Layout":
        confdir = "../xdb/coarsed_pruning_layout/configurations"
        tracedir = "../test_traces"
        confs = [conf for conf in os.listdir(confdir)]
    elif exp_name == "Coarsed_Non_Layout":
        confdir = "../xdb/coarsed_pruning/configurations"
        tracedir = "../test_traces"
        confs = [conf for conf in os.listdir(confdir)]
    elif exp_name == "Fine_Grained":
        confdir = "../xdb/fine_grained_pruning/configurations"
        tracedir = "../test_traces"
        confs = [conf for conf in os.listdir(confdir)]
    elif exp_name == "Verify_AIAgent":
        confdir = "../xdb/verify_aia/configurations"
        tracedir = "../autoblox_traces/test_traces"
        confs = [conf for conf in os.listdir(confdir)]
    else:
        print("No Matching exp_name.")
        exit()
    
    if target_name in ["LiveMapsBackEnd", "TPCC", "AdspayLoad", "WebSearch", "YCSB", "MapReduce", "CloudStorage"]:
        tracenames = []
        for trace in os.listdir(tracedir):
            if trace.startswith(target_name + "-") and not trace.endswith("-0-0-0"):
                tracenames.append(trace)
    elif target_name == "ALL":
        tracenames = []
        all_cats = ["LiveMapsBackEnd", "TPCC", "AdspayLoad", "WebSearch", "YCSB", "MapReduce", "CloudStorage"]
        for trace in os.listdir(tracedir):
            cat = trace.split("-")[0]
            if not cat in all_cats:
                continue
            if not trace.endswith("-0-0-0"):
                tracenames.append(trace)
    else:
        print("No Matching target_name.")
        exit()
    
    # batch_exec(confdir, tracedir, confs, tracenames)
    xdbTable_updates = {}
    # time_end = time.time()
    # print(f"Evaluation done, time spent {time_end - time_start}")
    for confname in confs:
        for t in tracenames:
            cat = t.split("-")[0]
            result = evaluate_config_workload(confdir + "/" + confname, tracedir + "/" + t)
            if not result: # This configuration is not valid, which cause the simulator to crase
                xdbTable_updates[confname] = "INVALID"
                break
            if confname not in xdbTable_updates:
                xdbTable_updates[confname] = {}
            xdbTable_updates[confname][cat] = {}
            xdbTable_updates[confname][cat][t] = [result[0], result[4], -1]
    baseline_conf = "baseline.xml"
    confname2cat = {
        "baseline.xml" : "Baseline",
        "batchanalysis.xml" : "MapReduce",
        "cloudstorage.xml" : "CloudStorage",
        "database.xml" : "TPCC",
        "kvstore.xml" : "YCSB",
        "livemaps.xml" : "LiveMapsBackEnd",
        "recomm.xml" : "AdspayLoad",
        "websearch.xml" : "WebSearch",
    }
    for confname in xdbTable_updates:
        if confname == baseline_conf:
            continue
        else:
            print("Evaluating configuration: ", confname)
            target_lat = 1
            target_tpt = 1
            nontarget_lat = 1
            nontarget_tpt = 1
            for cat in xdbTable_updates[confname]:
                avg_lat = 0
                avg_tpt = 0
                cnt = 0
                for tracename in xdbTable_updates[confname][cat]:
                    avg_lat += xdbTable_updates[confname][cat][tracename][0]
                    avg_tpt += xdbTable_updates[confname][cat][tracename][1]
                    cnt += 1
                if cnt > 0:
                    avg_lat /= cnt
                    avg_tpt /= cnt
                avg_lat_b = 0
                avg_tpt_b = 0
                cnt_b = 0
                for tracename in xdbTable_updates[baseline_conf][cat]:
                    avg_lat_b += xdbTable_updates[baseline_conf][cat][tracename][0]
                    avg_tpt_b += xdbTable_updates[baseline_conf][cat][tracename][1]
                    cnt_b += 1
                if cnt_b > 0:
                    avg_lat_b /= cnt_b
                    avg_tpt_b /= cnt_b
                perc_lat_improve = 0
                perc_tpt_improve = 0
                if confname2cat[confname] == cat:
                    target_lat = avg_lat_b / avg_lat
                    target_tpt = avg_tpt / avg_tpt_b
                else:
                    nontarget_lat *= avg_lat_b / avg_lat
                    nontarget_tpt *= avg_tpt / avg_tpt_b
                if avg_lat_b != 0:
                    perc_lat_improve = (avg_lat_b - avg_lat) / avg_lat_b
                if avg_tpt_b != 0:
                    perc_tpt_improve = (avg_tpt - avg_tpt_b) / avg_tpt_b
                print(f"{cat}, {perc_lat_improve:.2%}, {perc_tpt_improve:.2%}")
            nontarget_lat = nontarget_lat ** (1 / (len(xdbTable_updates[confname]) - 1))
            nontarget_tpt = nontarget_tpt ** (1 / (len(xdbTable_updates[confname]) - 1))
            print(f"Overall, {confname}, target_lat: {target_lat:.2%}, target_tpt: {target_tpt:.2%}, nontarget_lat: {nontarget_lat:.2%}, nontarget_tpt: {nontarget_tpt:.2%}")
            # a csv format
            print(f"{confname2cat[confname]}, {target_lat:.2%}, {target_tpt:.2%}, {nontarget_lat:.2%}, {nontarget_tpt:.2%}")
            print("---------------------------")

    print(xdbTable_updates)

