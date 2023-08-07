export target="TPCC"

mkdir ../xdb

# pruning

# coarsed pruning
mkdir ../xdb/coarsed_pruning
mkdir ../xdb/coarsed_pruning/configurations
mkdir ../xdb/coarsed_pruning/dram_trace
mkdir ../xdb/coarsed_pruning/warmup
mkdir ../xdb/coarsed_pruning/workloads
mkdir ../xdb/coarsed_pruning_layout
mkdir ../xdb/coarsed_pruning_layout/configurations
mkdir ../xdb/coarsed_pruning_layout/dram_trace
mkdir ../xdb/coarsed_pruning_layout/warmup
mkdir ../xdb/coarsed_pruning_layout/workloads
python3 generate_conf_coarsed_pruning_layout.py
python3 generate_conf_coarsed_pruning_non_layout.py
python3 batch_evaluation.py Coarsed_Layout TPCC
python3 batch_evaluation.py Coarsed_Layout YCSB
python3 batch_evaluation.py Coarsed_Layout LiveMapsBackEnd
python3 batch_evaluation.py Coarsed_Layout MapReduce
python3 batch_evaluation.py Coarsed_Layout WebSearch
python3 batch_evaluation.py Coarsed_Layout CloudStorage
python3 batch_evaluation.py Coarsed_Layout AdspayLoad
python3 batch_evaluation.py Coarsed_Non_Layout TPCC
python3 batch_evaluation.py Coarsed_Non_Layout YCSB
python3 batch_evaluation.py Coarsed_Non_Layout LiveMapsBackEnd
python3 batch_evaluation.py Coarsed_Non_Layout MapReduce
python3 batch_evaluation.py Coarsed_Non_Layout WebSearch
python3 batch_evaluation.py Coarsed_Non_Layout CloudStorage
python3 batch_evaluation.py Coarsed_Non_Layout AdspayLoad
python3 get_coarsed_pruning_data.py TPCC
python3 get_coarsed_pruning_data.py YCSB
python3 get_coarsed_pruning_data.py LiveMapsBackEnd
python3 get_coarsed_pruning_data.py MapReduce
python3 get_coarsed_pruning_data.py WebSearch
python3 get_coarsed_pruning_data.py CloudStorage
python3 get_coarsed_pruning_data.py AdspayLoad

cd ../reproduced_dat/
python3 coarsed_pruning.py
cd ../src

# fine-grained pruning
