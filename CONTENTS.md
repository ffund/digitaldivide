This repository includes:

* Python source code for the “digital divide” 
[tool](https://github.com/csmithsalzberg/digitaldivide/blob/master/src/digitaldivideutil.py) and 
[library](https://github.com/csmithsalzberg/digitaldivide/blob/master/src/digitaldivide.py). 
The code is released under the [MIT License](https://github.com/csmithsalzberg/digitaldivide/blob/master/LICENSE).
* An [installation script](https://github.com/csmithsalzberg/digitaldivide/blob/master/util/install.sh) that runs on Ubuntu 14.04 and installs `geni-lib` library and other prerequisites necessary to run the "digital divide" tool.
* A set of `bash` and `R` scripts that retrieve the raw data sources from the Internet 
and process them as described in Section II of our paper to produce our dataset of ≈ 8000 households, 
and generate Figure 2 and Figure 3. (Note: requires [gnumeric](http://packages.ubuntu.com/gnumeric).)
* The [dataset](https://github.com/csmithsalzberg/digitaldivide/blob/master/dat/household-internet-data.csv) 
of approximately 8000 households, in CSV format. 
* A set of `bash` and `R` scripts and instructions to run the experiment and generate the figures of 
Section IV in our paper.

