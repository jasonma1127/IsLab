#!/bin/bash

usage() {
    echo "Run the script with"
    echo "  $ bash $0 [-d <directory>] [-f <file>] [-l <file>]"
    echo
    echo "    -d    The directory with binaries to be reversed"
    echo "    -f    The file to be reversed"
    echo "    -l    The file with a list of files to be reversed"
}

rev_run() {
    # fname=$(basename $1)
    echo "[RUN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $1"
}

rev_fin() {
    # fname=$(basename $1)
    echo "[FIN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $1"
}

reverse() {
    # TIMEOUT=180
    TIMEOUT=3600
    STATE_LIST="./state_log"
    # source reverse.conf
    # [[ $1 == '' ]] && echo 'File Path not provided' && exit 1
    # if [[ $1 != '' ]] && [[ $2 != '' ]] && [[ $3 != '' ]]; then
    #     echo "Input invalid"
    #     exit 1
    # fi
    # fpath=$1
    fname=$3

    # rev_run $fpath
    rev_run $fname

    # main section
    # timeout --kill-after=5s "$TIMEOUT"s \
    #     python $MAIN_SCRIPT -f $fpath -o $FCG_DIR 2> "$LOG_DIR/$(basename $fpath).log"
    # echo "$fpath,$?" >> $STATE_LIST  # $? records the state after reversing (fail or success)

    timeout --kill-after=5s "$TIMEOUT"s \
        python new_extractOpcode_retdec.py -i $1 -o $2 -f $fname
    echo "$fname,$?" >> $STATE_LIST  # $? records the state after reversing (fail or success)

    # rev_fin $fpath
    rev_fin $fname
}

STATE_LIST="./state_log"
WORKERS=30

# [[ $(pip list | grep r2pipe > /dev/null)$? -eq 1 ]] && echo "No module named 'r2pipe'" && exit 1

[[ $1 == '' ]] && usage && exit 0
# mkdir -p $FCG_DIR
# mkdir -p $LOG_DIR

[[ -f $STATE_LIST ]] && rm $STATE_LIST
touch $STATE_LIST

input_dir=$1
output_dir=$2
file_list=$3

export -f reverse
export -f rev_run
export -f rev_fin

# echo $input_dir
# echo $output_dir
cat $file_list | xargs -P $WORKERS -I {} bash -c "reverse $input_dir $output_dir {}"


# while getopts "hd:f:l:" argv; do
#     case $argv in
#         h )
#             usage
#             exit 0
#             ;;
        
#         d )
#             dir=$OPTARG
#             [[ -d $dir ]] || (echo 'Invalid Directory' && usage && exit 1)

#             if [[ $SHUFFLE -eq 1 ]]; then
#                 comm -3 <(find $dir -type f | sort) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | shuf | \
#                     xargs -P $WORKERS -I {} bash -c "reverse {}"
#             else
#                 comm -3 <(find $dir -type f | sort) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | \
#                     xargs -P $WORKERS -I {} bash -c "reverse {}"
#             fi
#             ;;

#         f )
#             file=$OPTARG
#             # [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
#             bash -c "reverse $file"
#             ;;

#         l )
#             list=$OPTARG
#             [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)

#             if [[ $SHUFFLE -eq 1 ]]; then
#                 comm -3 <(sort $list) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | shuf | \
#                     xargs -P $WORKERS -I {} bash -c "reverse {}"
#             else
#                 comm -3 <(sort $list) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | \
#                     xargs -P $WORKERS -I {} bash -c "reverse {}"
#             fi
#             ;;

#         ? )
#             usage
#             exit 1
#             ;;
#     esac
# done