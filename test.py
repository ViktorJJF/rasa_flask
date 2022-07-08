import json
from tkinter import Y
import yaml
from collections import OrderedDict

# yaml_file=open('./bots/1/data/nlu.yml','r', encoding = "utf-8")
# print(yaml_file.read())
# data = yaml.load(yaml_file, Loader=yaml.FullLoader)
# print(json.dumps(data, indent=4, ensure_ascii=False))
# print("Mu deep data {}".format(data['intents']))


# # Based on Any yaml libraries in Python that support dumping of long strings as block literals or folded blocks?

# import yaml
# from collections import OrderedDict

class quoted(str):
    pass

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
yaml.add_representer(quoted, quoted_presenter)

class literal(str):
    pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
yaml.add_representer(literal, literal_presenter)

def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(OrderedDict, ordered_dict_presenter)

# # # d = OrderedDict(short=quoted("Hello"), long=literal("Line1\nLine2\nLine3\n"))

# # dump_yml=yaml.dump({'name':'My first question','phrases':literal("Frase 1\nFrase 2\nFrase 3\n")})
# # print("Hecho! {}".format(dump_yml))

# # yaml.dump(dump_yml, file, default_flow_style = False, allow_unicode = True, encoding = None)
# # file.close()

# dict_file = OrderedDict(sports= ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis'],
# countries=literal("jaja\nxd"))

file = open("test2.yml", "w", encoding = "utf-8")
data = open("nlu.json", "r", encoding = "utf-8")
yaml.dump(json.load(data), file, default_flow_style=False)
file.close()

# # print(dict_file)
# # with open(r'./store_file.yaml', 'w') as file:
# #     documents = yaml.dump(dict_file, file)
