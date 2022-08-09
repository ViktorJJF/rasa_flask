import json
from collections import OrderedDict
from tkinter import Y

import yaml

yaml_file=open('./bots/1/data/nlu.yml','r', encoding = "utf-8")
# print(yaml_file.read())
# data = yaml.load(yaml_file, Loader=yaml.FullLoader)
# print(json.dumps(data, indent=4, ensure_ascii=False))
# print("Mu deep data {}".format(data['intents']))


# # Based on Any yaml libraries in Python that support dumping of long strings as block literals or folded blocks?

# import yaml
# from collections import OrderedDict

# class quoted(str):
#     pass

# def quoted_presenter(dumper, data):
#     return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
# yaml.add_representer(quoted, quoted_presenter)

# class literal(str):
#     pass

# def literal_presenter(dumper, data):
#     return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
# yaml.add_representer(literal, literal_presenter)

# def ordered_dict_presenter(dumper, data):
#     return dumper.represent_dict(data.items())
# yaml.add_representer(OrderedDict, ordered_dict_presenter)

# # # d = OrderedDict(short=quoted("Hello"), long=literal("Line1\nLine2\nLine3\n"))

# dump_yml=yaml.dump({'name':'My first questin'})
# print("Hecho! {}".format(dump_yml))
# file = open("test2.yml", "w", encoding = "utf-8")
# yaml.dump(dump_yml, file, default_flow_style = False, allow_unicode = True, encoding = None)
# file.close()

# dict_file = OrderedDict(sports= ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis'],
# countries=literal("jaja\nxd"))

# data = open("nlu.json", "r", encoding = "utf-8")
# file = open("test2.yml", "w", encoding = "utf-8")
# yaml.dump(yaml.load(data), file, default_flow_style=False)
# file.close()

# nlu_path="./bots/base/data/nlu.yml"
# nlu_file=open(nlu_path,"r+", encoding = "utf-8")
# # json representation
# nlu_json=yaml.safe_load(nlu_file)
# print('nlu_json: ', json.dumps(nlu_json,ensure_ascii=False))
# # yml representation
# nlu_yml=yaml.dump(nlu_json)
# # writing on file
# nlu_file.seek(0)
# nlu_file.write(nlu_yml)
# nlu_file.truncate()
# nlu_file.close()
# print("HECHO!")

def json_to_yml_file(path_file):
    json_file=open(path_file,"r", encoding = "utf-8")
    json_payload = json.load(json_file)
    file = open(path_file.replace(".json", ".yml"), 'w+', encoding = "utf-8")
    yaml.dump(json_payload, file,default_flow_style = False, allow_unicode = True, encoding = "utf-8")
    json_file.close()
    file.close()
    print("JSON A YML CREADO! ")

def yml_to_json_file(path_file):
    yml_file=open(path_file,"r", encoding = "utf-8")
    yml_payload = yaml.safe_load(yml_file)
    file = open(path_file.replace(".yml", ".json"), 'w+', encoding = "utf-8")
    json.dump(yml_payload, file,ensure_ascii=False)
    yml_file.close()
    file.close()
    print("YML A JSON CREADO! ")
    
#     data = open("nlu.json", "r", encoding = "utf-8")
# file = open("test2.yml", "w", encoding = "utf-8")
# yaml.dump(yaml.load(data), file, default_flow_style=False)
# file.close()

json_to_yml_file("./bots/base/domain.json")
# yml_to_json_file("./bots/base/domain.yml")
    


# with open(nlu_path, 'r') as nluData, open(nlu_path, "w") as json_out:
#     domain=open("./bots/base/domain.yml", 'r', encoding = "utf-8")
#     nlu = yaml.safe_load(nluData) # yaml_object will be a list or a dict
#     # convert yml to json
#     domain=yaml.safe_load(domain)
#     # reconvert json to yml
#     print(f"El dominio: {nlu}")
#     members = [{'name': 'Zoey', 'occupation': 'Doctor'},
#            {'name': 'Zaara', 'occupation': 'Dentist'}]
#     # print(yaml.dump(nlu))
#     json.dump(nlu, json_out, ensure_ascii=False)

# # print(dict_file)
# # with open(r'./store_file.yaml', 'w') as file:
# #     documents = yaml.dump(dict_file, file)
