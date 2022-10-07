import json
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('base_dir:',base_dir)
def read_config(param):
    if param == 'db_config':
        with open(base_dir + '/config/db_config.json','r') as f:
            config_param = json.load(f)
        return config_param
db_config=read_config('db_config')
if __name__ == '__main__':
    config_param = read_config('db_config')
    print(config_param)
