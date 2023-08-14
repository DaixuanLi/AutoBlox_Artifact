export xdb_dir=../xdb
mkdir $xdb_dir
mv ../xdb_base $xdb_dir
cd $xdb_dir
# pruning exps
mkdir coarsed_pruning
cd coarsed_pruning
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir coarsed_pruning_layout
cd coarsed_pruning_layout
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir fine_grained_pruning
cd fine_grained_pruning
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_TPCC
cd nvme_mlc_TPCC
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_YCSB
cd nvme_mlc_YCSB
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_WebSearch
cd nvme_mlc_WebSearch
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_LiveMapsBackEnd
cd nvme_mlc_LiveMapsBackEnd
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_AdspayLoad
cd nvme_mlc_AdspayLoad
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_CloudStorage
cd nvme_mlc_CloudStorage
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..
mkdir nvme_mlc_MapReduce
cd nvme_mlc_MapReduce
mkdir configurations
mkdir dram_trace
mkdir warmup
mkdir workloads
cp ../xdb_base/configurations/* configurations
cp ../xdb_base/warmup/* warmup
cp ../xdb_base/status_file/* .
cd ..