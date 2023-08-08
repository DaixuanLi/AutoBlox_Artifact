# AutoBlox_Artifact

Artifact of paper Learning to Drive Software-Deﬁned Solid-State Drives to appear in MICRO'23.

## Artifact Introduction

AutoBlox is a learning framework to assist the design of Software-Defined SSDs. Specifically, AutoBlox can efficiently identify optimized configurations for target workloads with constraints (Host Interface, Capacity, Power).

## Dependencies Installation 

AutoBlox requires psutil, scikit-learn, numpy and seaborn packages. 

Please use
```
cloudlab_server_setup_instructions.sh
```
to install dependencies.

Please download the traces from [will be updated soon].

## Running the Experiments

Before running the experiments, we first need to setup the xdb Tables.

```
src/setup_xdb.sh
```

Then, we can start reproducing the figures.

### Workload Clustering (Figure 2)

To reproduce Figure 2 in the paper, please run 

```
cd src
python3 clustering_motivaltion.py
cd ../reproduced_dat
python3 clustering.py
```

The workload clustering figure will appear in reproduced_dat folder. The figure proves that AutoBlox can efficiently identify new workloads.


### Fine-grained and Coarsed-grained Pruning (Figure 3, 4)

To reproduce Figure 3 and 4,  please run

```
cd src/
run_pruning.sh -w target_workload
```

Here target_workload has 7 options (YCSB, TPCC, AdspayLoad, MapReduce, LiveMapsBackEnd, WebSearch, and CloudStorage). It takes approximately 2-4 hour for each workload to finish its pruning. We will provide several cloud lab nodes to run the pruning in parallel.

After the pruning is finished, please run

```
cd reproduced_dat/
python3 fine_grained_pruning.py
python3 coarsed_pruning.py
```

Then,  Figure 3,4 will appear in the reproduced_dat folder. in the paper.

### Training (We reproduce Table 1, Figure 7, 8 as examples)

To train for a given workload type and with/without tuning order, please use

```
cd src
find_best_conf.py target_workload use_tuning_order xdb_directory
```

for training each workload. Here target_workload has 7 options (YCSB, TPCC, AdspayLoad, MapReduce, LiveMapsBackEnd, WebSearch, and CloudStorage), and use_tuning_order has two options (True and False). It takes approximately 12 hour for each workload to finish its training. We will provide several cloud lab nodes to run the training in parallel, and xdb_directory is the shared xdb folder within the cloud lab cluster we provided.

After the training, the log files should be stored in xdb/ folder. 

To reproduce Table 1, we run:

```
python3 get_recommended_configurations.py xdb_directory
```

Table 1 should appear in reproduced_dat folder.

To plot the training procedure Figure 7 and Figure 8, run 

```
python3 profile_training.py xdb_directory
cd ../reproduced_dat
python3 learning_profile.py
python3 tuning_time.py
```

Figure 7 and 8 should appear in reproduce_dat/ folder. This figure shows that with enforced tuning order, AutoBlox can accelerate the training procedure.



