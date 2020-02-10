import networkx as nx
import util.nx_extract as nxe
from inspect import getmembers, isfunction, signature

if __name__ == "__main__":
    for m in getmembers(nx):
        if isfunction(m[1]):
            args = signature(m[1])
            print(args)
            md = nxe.get_member_metadata(m)
            print(md)
