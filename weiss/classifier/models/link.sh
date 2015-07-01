#!/bin/bash
date=$(date +%Y-%m-%d)
DIR=/home/wenjunw/Weiss/classifier/models/
modelname=$DIR"model_"$date
featurename=$DIR"features_"$date

link1="ln -s action_model "$modelname
eval "$link1"
link2="ln -s action_features "$featurename
eval "$link2"
