#!/bin/bash
echo "import networkx as nx" > $1
echo "import networkx as nx" >> $1
echo "from typing import *" >> $1
echo "from types import *" >> $1
echo "from numbers import *" >> $1
echo "import numpy as np" >> $1
python3 util/wrap_nx_with_types.py >> $1