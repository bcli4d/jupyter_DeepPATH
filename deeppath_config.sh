sudo apt-get install -y git virtualenv
virtualenv $HOME/dp
source $HOME/dp/bin/activate
sudo apt-get install -y libopenslide0

#Get the DeepPATH code if not already installed
if [ ! -d $HOME/DeepPATH]; then
      git -C $HOME clone -b whc1 https://github.com/bcli4d/DeepPATH.git 
fi
pip install jupyter
pip install jupyter_tensorboard
pip install jupyterlab
pip install nbdime
pip install openslide-python
pip install dicom
pip install google-cloud-storage
pip install numpy
pip install scipy
pip install tensorflow-gpu
pip install matplotlib
pip install sklearn

pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install
