#!/bin/sh

# Install conda packages for eva_api
conda env create -f script/install/conda_eva_api_environment.yml
. activate eva_api
conda list


