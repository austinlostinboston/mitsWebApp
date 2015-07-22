#!/bin/bash
#This file will link file named action_model and action_features
#which are in the same directory as this one to the feature file
#model file under the directory of /home/wenjunw/Weiss/classifier/models/
#Feature and model files under the destination directory is updated
#everyday.
#
#Author: Wenjun Wang<wenjunw@cs.cmu.edu>
#Date: July 1, 2015
date=$(date +%Y-%m-%d)
DIR=/home/wenjunw/Weiss/classifier/models/
modelname=$DIR"model_"$date
featurename=$DIR"features_"$date

link1="ln -s action_model "$modelname
eval "$link1"
link2="ln -s action_features "$featurename
eval "$link2"
