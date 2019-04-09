#!/bin/bash

set -x


export CHECKPOINT_PATH=/mnt/disks/deeppath-data/intermediate_checkpoints
CHECKPOINT_PATH=/mnt/disks/deeppath-data/intermediate_checkpoints
export OUTPUT_DIR=/mnt/disks/deeppath-data/evaluations
OUTPUT_DIR=/mnt/disks/deeppath-data/evaluations
export DATA_DIR=/mnt/disks/deeppath-data/Data/images/TFRecord_TrainValid
DATA_DIR=/mnt/disks/deeppath-data/Data/images/TFRecord_TrainValid
export LABEL_FILE=/mnt/disks/deeppath-data/Data/images/sorted/data_labels
LABEL_FILE=/mnt/disks/deeppath-data/Data/images/sorted/data_labels
export NC_IMAGENET_EVAL=/home/bcliffor/DeepPATH/DeepPATH_code/s02_testing/xClasses/nc_imagenet_eval.py
NC_IMAGENET_EVAL=/home/bcliffor/DeepPATH/DeepPATH_code/s02_testing/xClasses/nc_imagenet_eval.py
export BOOTSTRAP=/home/bcliffor/DeepPATH/DeepPATH_code/s03_postprocessing/v0h_ROC_MultiOutput_BootStrap.py
BOOTSTRAP=/home/bcliffor/DeepPATH/DeepPATH_code/s03_postprocessing/v0h_ROC_MultiOutput_BootStrap.py
#export NbClasses=3
#NbClasses=3
'''
export CHECKPOINT_PATH=$1
export OUTPUT_DIR=$2
export DATA_DIR=$3
export LABEL_FILE=$4
export NC_IMAGENET_EVAL=$5
export BOOTSTRAP=$6
#export NbClasses=$7
#module load python/gpu/3.6.5
'''

# create temporary directory for checkpoints
mkdir  -p $OUTPUT_DIR/tmp_checkpoints
export CUR_CHECKPOINT=$OUTPUT_DIR/tmp_checkpoints


# check if next checkpoint available
declare -i count=10000
declare -i step=5000
declare -i NbClasses=3

while true; do
    echo $count
    if [ -f $CHECKPOINT_PATH/model.ckpt-$count.meta ]; then
	echo $CHECKPOINT_PATH/model.ckpt-$count.meta " exists"
	# check if there's already a computation for this checkpoinmt
	export TEST_OUTPUT=$OUTPUT_DIR/test_$count'k'
	if [ ! -d $TEST_OUTPUT ]; then
	    mkdir -p $TEST_OUTPUT


	    ln -s $CHECKPOINT_PATH/*-$count.* $CUR_CHECKPOINT/.
	    touch $CUR_CHECKPOINT/checkpoint
	    echo 'model_checkpoint_path: "'$CUR_CHECKPOINT'/model.ckpt-'$count'"' > $CUR_CHECKPOINT/checkpoint
	    echo 'all_model_checkpoint_paths: "'$CUR_CHECKPOINT'/model.ckpt-'$count'"' >> $CUR_CHECKPOINT/checkpoint

	    # Test
	    python $NC_IMAGENET_EVAL --checkpoint_dir=$CUR_CHECKPOINT --eval_dir=$OUTPUT_DIR --data_dir=$DATA_DIR \
		   --batch_size 80  --run_once --ImageSet_basename='valid_' --ClassNumber $NbClasses --mode='0_softmax'  --TVmode='test' > /tmp/log/nc_imagenet_eval.log 2>&1
	    # wait

	    mv $OUTPUT_DIR/out* $TEST_OUTPUT/.

	    # ROC
	    export OUTFILENAME=$TEST_OUTPUT/out_filename_Stats.txt
#	    export OUTFILENAME=$TEST_OUTPUT/out_All_Stats.txt
	    python $BOOTSTRAP --file_stats=$OUTFILENAME  --output_dir=$TEST_OUTPUT --labels_names=$LABEL_FILE > /tmp/log/bootstrap.log 2>&1                  

	else
	    echo 'checkpoint '$TEST_OUTPUT' skipped'
	fi

    else
	echo $CHECKPOINT_PATH/model.ckpt-$count.meta " does not exist"
	break
    fi

    # next checkpoint
    count=`expr "$count" + "$step"`
done

# summarize all AUC per slide (average probability) for class 1:
ls -tr $OUTPUT_DIR/test_*/out2_roc_data_AvPb_c1*  | sed -e 's/k\/out2_roc_data_AvPb_c1/ /' | sed -e 's/test_/ /' | sed -e 's/_/ /g' | sed -e 's/.txt//'   > $OUTPUT_DIR/valid_out2_AvPb_AUCs_1.txt


# summarize all AUC per slide (average probability) for macro average:
ls -tr $OUTPUT_DIR/test_*/out2_roc_data_AvPb_macro*  | sed -e 's/k\/out2_roc_data_AvPb_macro_/ /' | sed -e 's/test_/ /' | sed -e 's/_/ /g' | sed -e 's/.txt//'   > $OUTPUT_DIR/valid_out2_AvPb_AUCs_macro.txt


# summarize all AUC per slide (average probability) for micro average:
ls -tr $OUTPUT_DIR/test_*/out2_roc_data_AvPb_micro*  | sed -e 's/k\/out2_roc_data_AvPb_micro_/ /' | sed -e 's/test_/ /' | sed -e 's/_/ /g' | sed -e 's/.txt//'   > $OUTPUT_DIR/valid_out2_AvPb_AUCs_micro.txt

ls -tr $OUTPUT_DIR/test_*/out2_roc_data_AvPb_c2*  | sed -e 's/k\/out2_roc_data_AvPb_c2/ /' | sed -e 's/test_/ /' | sed -e 's/_/ /g' | sed -e 's/.txt//'   > $OUTPUT_DIR/valid_out2_AvPb_AUCs_2.txt

ls -tr $OUTPUT_DIR/test_*/out2_roc_data_AvPb_c3*  | sed -e 's/k\/out2_roc_data_AvPb_c3/ /' | sed -e 's/test_/ /' | sed -e 's/_/ /g' | sed -e 's/.txt//'   > $OUTPUT_DIR/valid_out2_AvPb_AUCs_3.txt
