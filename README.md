# jupyter_DeepPATH

## Overview

This repo holds a notebook that is intended to reproduce the results reported in this paper: https://www.nature.com/articles/s41591-018-0177-5. However, whereas the implementation reported in the paper obtains pathology images from TCIA, and mutation calls from the GDC, this implentation uses ISB-CGC metadata in Google BigQuery to determine pathology images and their corresponding tumor type and mutation calls. It then obtains pathology images from an ISB-CGC maintained GCS bucket.

See the notebook intro for more details

## Installation and execution

Because of the computational requirements, this notebook needs to be run on a (Google) VM with one or more GPUs. We recommend running on a VM which is configured with one of the Google "Deep Learning" images such as `Deep Learning Image: TensorFlow 1.14.0 m314` (or similar), and which come with CUDA and tensorflow pre-installed. After cloning this repo to the VM, execute deeppath_config.sh to configure the enviroment, and then start the jupyter server:

 `$ git clone https://github.com/bcli4d/jupyter_DeepPATH.git`

 `$ ./jupyter_DeepPATH/deeppath_config.sh`

 `$ ./jupyter_DeepPATH/start_jupyter.sh`

Note that you will need to configure SSH port forwarding or use some other mechanism to be able to securely open the notebook in your browser.
