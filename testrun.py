#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ingress_agent_data_recover as iadr

text_corrupted_list = [
]

text_recovered_list = {}

for text_corrupted in text_corrupted_list:
    agent_data = iadr.parse_agent_data_corrupted(text_corrupted)
    if not agent_data:
        print("Failed processing data:")
        print(text_corrupted)
        continue
    text_recovered = iadr.format_agent_data(agent_data)
    text_recovered_list[agent_data["Agent Name"]] = text_recovered

for user, text in text_recovered_list.items():
    with open(f"{user}.csv", "w") as fp:
        fp.write(text)

