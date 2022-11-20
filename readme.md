##  To install
py -m venv venv
venv\Scripts\activate
pip install --upgrade pip

pip install -r https://www.comp.hkbu.edu.hk/~mandel/comp7510/pkg.txt
source ur.venv.name/bin/activate  (mac)
py -m ensurepip
pip install -r package.txt


## To run 

python example.py


## Mac version ##
py -m venv venv
. ./venv/bin/activate
pip install --upgrade pip

### Emulated x86 for M1 Mac (JT: for my ref only )
arch -x86_64 /bin/bash
pip install -r https://www.comp.hkbu.edu.hk/~mandel/comp7510/pkg.txt
. ./venv/bin/activate
python -m ensurepip
pip install -r package.txt

python main.py --size=200x300 --dpi=271

#pip install email-validator