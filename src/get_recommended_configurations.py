import sys

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv) != 2:
    print("Usage: python3 get_recommended_configurations.py xdb_directory")
    exit()

# extract recommended configurations

target_workloads = ["TPCC", "WebSearch", "CloudStorage", "LiveMapsBackEnd", "AdspayLoad", "MapReduce", "YCSB"]

if target_workload not in :
    print(f"workload target {target_workload} not exist.")

