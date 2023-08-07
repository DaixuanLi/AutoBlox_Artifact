# AutoBlox_Artifact

Artifact of paper Learning to Drive Software-Deﬁned Solid-State Drives to appear in MICRO'23.

## Artifact Introduction

AutoBlox is a learning framework that assist the design of Software-Defined SSDs. Specifically, AutoBlox can efficiently identify optimized configuration for target workloads with given constraints (Host Interface, Capacity, Power).

## Dependencies Installation 

AutoBlox require psutil, scikit-learn and numpy packages. 

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

Then, we can perform the following functionalities.

### Workload Clustering

To cluster the workload, please run 

```
src/clustering_motivaltion.py
src/clustering.py
```
The workload clustering result will appear in reproduced_dat folder.


### Fine-grained and Coarsed-grained Pruning

To run coarsed_grained and fine_grained pruning, please use 

```
src/run_pruning.sh target_workload
```

It takes approximately 2-4 hour for each workload to finish its pruning. We provide several cloud lab nodes to run the pruning in parallel.

```
reproduced_dat/fine_grained.py
reproduced_dat/coarsed_pruning.py
```
Then, can reproduce the Figure 3,4 in the paper.

### Training

To train for a given workload type and with/without tuning order, please use

```
cd src
find_best_conf.py target_workload use_tuning_order
```
for training each workload.

Then, use 

```
batch_evaluation.py TEST_TRAINING
```

to test the optimized configuration proposed by AutoBlox.

Finally, use 

```
profile_training.sh
```

to plot the training procedure figure.

The training for each workload may take less than 12 hours, it is highly recommended to run each target workload separately.


