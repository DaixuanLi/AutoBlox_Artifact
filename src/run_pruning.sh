python3 generate_conf_coarsed_pruning_layout.py
python3 generate_conf_coarsed_pruning_non_layout.py
python3 generate_fine_grained_pruning.py
python3 batch_evaluation.py Coarsed_Layout $target
python3 batch_evaluation.py Coarsed_Non_Layout $target
python3 batch_evaluation.py Fine_Grained $target
python3 get_coarsed_pruning_data.py $target
python3 get_fine_grained_pruning_data.py $target