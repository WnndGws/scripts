#!/usr/bin/env zsh
# https://www.cubicrace.com/2016/03/efficient-logging-mechnism-in-shell.html

SCRIPT_LOG="$HOME"/shell_script.log
touch $SCRIPT_LOG

function SCRIPTENTRY(){
    timeAndDate=$(date)
    script_name=$(basename "$0")
    script_name="${script_name%.*}"
    echo "[$timeAndDate] [DEBUG]  > $script_name $FUNCNAME" >> $SCRIPT_LOG
}

function SCRIPTEXIT(){
    script_name=$(basename "$0")
    script_name="${script_name%.*}"
    echo "[$timeAndDate] [DEBUG]  < $script_name $FUNCNAME" >> $SCRIPT_LOG
}

function ENTRY(){
    local cfn="${FUNCNAME[1]}"
    timeAndDate=$(date)
    echo "[$timeAndDate] [DEBUG]  > $cfn $FUNCNAME" >> $SCRIPT_LOG
}

function EXIT(){
    local cfn="${FUNCNAME[1]}"
    timeAndDate=$(date)
    echo "[$timeAndDate] [DEBUG]  < $cfn $FUNCNAME" >> $SCRIPT_LOG
}


function INFO(){
    local function_name="${FUNCNAME[1]}"
    local msg="$1"
    timeAndDate=$(date)
    echo "[$timeAndDate] [INFO]  $msg" >> $SCRIPT_LOG
}


function DEBUG(){
    local function_name="${FUNCNAME[1]}"
    local msg="$1"
    timeAndDate=$(date)
    echo "[$timeAndDate] [DEBUG]  $msg" >> $SCRIPT_LOG
}

function ERROR(){
    local function_name="${FUNCNAME[1]}"
    local msg="$1"
    timeAndDate=$(date)
    echo "[$timeAndDate] [ERROR]  $msg" >> $SCRIPT_LOG
}
