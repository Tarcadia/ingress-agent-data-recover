# -*- coding: utf-8 -*-

import re

from ._agent_data import INGRESS_AGENT_DATA_FIELD_MAP

INGRESS_AGENT_DATA_LINE_BREAK = "\n"
INGRESS_AGENT_DATA_FIELD_BREAK = "\t"
INGRESS_AGENT_DATA_FIELD_BREAK_CORRUPTED = "\\s*"


def parse_agent_data_corrupted(agent_data_text: str):
    lines = [line for line in agent_data_text.splitlines() if line]
    if not lines:
        return {}
    if len(lines) != 2:
        return {}
    
    _line_fields, _line_values = lines
    _idx_fields = sorted(
        (_i, _f)
        for _f in INGRESS_AGENT_DATA_FIELD_MAP
        if (_i:=_line_fields.find(_f)) >= 0
    )
    _patt_fields = "".join(
        f"({re.escape(_f)}){INGRESS_AGENT_DATA_FIELD_BREAK_CORRUPTED}"
        for _, _f in _idx_fields
    )
    _patt_values = "".join(
        f"({INGRESS_AGENT_DATA_FIELD_MAP[_f]}){INGRESS_AGENT_DATA_FIELD_BREAK_CORRUPTED}"
        for _, _f in _idx_fields
    )
    _fields = re.findall(_patt_fields, _line_fields)
    _values = re.findall(_patt_values, _line_values)
    if not all([_fields, _values]):
        return {}

    agent_data_dict = {
        _field: _value
        for _field, _value in zip(_fields[0], _values[0])
    }
    return agent_data_dict


def format_agent_data(agent_data_dict: dict):
    _line_fields = INGRESS_AGENT_DATA_FIELD_BREAK.join(agent_data_dict.keys()) + INGRESS_AGENT_DATA_FIELD_BREAK
    _line_values = INGRESS_AGENT_DATA_FIELD_BREAK.join(agent_data_dict.values()) + INGRESS_AGENT_DATA_FIELD_BREAK
    return INGRESS_AGENT_DATA_LINE_BREAK.join([_line_fields, _line_values])