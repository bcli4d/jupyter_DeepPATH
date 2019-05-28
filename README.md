# jupyter_DeepPATH

## Overview

This repo holds several notebooks that are intended to reproduce the results in report in this paper: https://www.nature.com/articles/s41591-018-0177-5. However, whereas the implementation reported in the paper obtains pathology images from TCIA, and mutation calls from the GDC, this implentation uses ISB-CGC metadata in BQ to determine pathology images and their corresponding tumor type and mutation calls. It then obtains pathology images from a ISB-CGC maintained GCS bucket.

There are currently several notebooks:

* _DeepPATH; Normal, LUAD, LUSC classification; transfer learning.ipynb_ uses transfer learning with TCGA_LUAD and TCGA_LUSC "frozen tissue" slides to classify for normal, LUAD, and LUSC.

* _DeepPATH; Mutation classification; fully trained; non-silent mutations.ipynb_ is intended to classify mutations ofTCGA_LUAD frozen tissue images. It is currently a work in progress.

Additional notebooks can be ignored at this time. The notebooks are supported by a few scripts to aid running DeepPATH in jupyter.

The pipeline is divided roughly into three phases: tiling, sorting, training and evaluation, and there is a parameterization cell for each phases. In addition to controlling computation, (some of) the parameters of each phase are used to define a directory name in which compution data is stored, and the various directories form a hierarchy. 

The first cell in each phase, if executed, will restore results of a previous computation of that phase form GCS, if those results were previously saved to GCS. The last cell of each phase can optionally be executed for that purpose. Any such saved results are maintained in a similar hierarchy in the designated GCS bucket.

## Installation and execution

Because of the computational requirements, this notebook needs to be run on a VM with one or more GPUs.

Clone this repo to a VM which is configured with Cuda, such as the `c2-deeplearning-tf-1-13-cu100-20190314` GCP image,
then execute deeppath_config.sh, and start jupyter:

 `$ git clone https://github.com/bcli4d/jupyter_DeepPATH.git`

 `$ ./jupyter_DeepPATH/deeppath_config.sh`

 `$ ./jupyter_DeepPATH/start_jupyter.sh`
