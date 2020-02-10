import networkx as nx
from inspect import getmembers, isfunction, getargspec
from docstring_parser import parse
import re
from typing import Tuple, Dict, List, Any

PARAMETERS = "Parameters"
RETURNS = "Returns"
SEE = "See"


class FunctionMetadata(object):
    def __init__(self, name: str, ast: Dict, doc: str):
        super().__init__()
        self.name = name
        self.parameters = ast.get(PARAMETERS, {})
        self.returns = ast.get(RETURNS, {})
        self.doc = doc

    def __repr__(self):
        return f"{self.name}: {self.parameters} -> {self.returns}"


def clean_doc(doc: str) -> str:
    cleaned = ""
    for line in doc.split("\n"):
        line = clean_line(line)
        cleaned += line + "\n"
    return cleaned


def clean_line(line: str):
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s+:", ":", line)
    # line = re.sub(r"\n", "", line)
    line = re.sub(r"^\s+", "", line)
    return line


def get_sections(doc: str) -> Dict:
    lines = doc.split("\n")
    section_pos = []
    for i, line in enumerate(lines):
        if re.match("^\-+", line):
            section_pos.append(i - 1)
    # print(section_pos)
    sections = {}
    for i, pos in enumerate(section_pos):
        section_name = lines[pos]
        start_pos = pos + 2
        if i < len(section_pos) - 1:
            end_pos = section_pos[i + 1]
            section_content = lines[start_pos:end_pos]
        else:
            section_content = lines[start_pos:]
        sections[section_name] = section_content
    return sections


def get_parameters(section_content: List[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    param = None
    for line in section_content:
        match = re.search(r"^(\w+):\s*(.*)$", line)
        if match:
            param = match.group(1)
            # Nx docs may have a "See: NNNNN" section that is not a parameter. It must be removed
            if param != SEE:
                params[param] = match.group(2)
        elif param and line:
            if param != SEE:
                params[param] += " " + line

    return params


def parse_nx_doc(doc: str) -> Dict[str, Any]:
    doc = clean_doc(doc)
    # print(doc)
    section = get_sections(doc)
    ast: Dict[str, Any] = {}
    for section_name, content in section.items():
        if section_name == PARAMETERS:
            p = get_parameters(content)
            ast[section_name] = p
        elif section_name == RETURNS:
            ast[section_name] = " ".join(content)
    return ast


def get_member_metadata(m: Tuple):

    if isfunction(m[1]):
        doc = m[1].__doc__
        if doc:
            ast = parse_nx_doc(doc)
            return FunctionMetadata(m[0], ast, doc)


if __name__ == "__main__":
    for m in getmembers(nx):
        md = get_member_metadata(m)
        print(md)

    md = get_member_metadata(getmembers(nx)[121])
    print(md)

    md = get_member_metadata(("w", nx.watts_strogatz_graph))
    print(md)
