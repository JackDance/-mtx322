import os
import csv
import datetime
import json

# def json_load(json_path):
#     with open (json_path, 'rb') as f:
#         json_content = json.load(f)
#         for i in json_content:
#             print(i)
#
# if __name__ == '__main__':
#     json_path = './eval_res.json'
#     json_load(json_path)


def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    print(ret_dic)

if __name__ == '__main__':
    input_json = r'./instances_val2017.json'
    parse_para(input_json)

