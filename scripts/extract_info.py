import re
import json
import sys
from pprint import pprint

with open("data.txt", 'r') as f:

    g = open('result.out', 'w')  # save determining information inside a file

    for line in f:
        # search for the line in the data that begins with 'uname'
        searched = re.search(pattern=r'^(uname)', string=line)
        if searched:  # Not None
            # collect data inside ()
            conf = re.search(pattern=r'\((.*)\)', string=line)
            data = conf.groups()[0]  # save configuration data
            print(f'span = {conf.span()} and the matched string = {data}')
            g.write(data)
            g.write('\n')
            break  # no need to loop through all the content of the file

# reformatting to use prepare for json operations
parsed_data = '{"' + re.sub(', ', ', "', re.sub(r'=', r'":', data)) + '}'
parsed_data = parsed_data.replace("'", '"')
print(parsed_data)  # test reformtting result

# parsed_data = '{"id":1, "name":"Mr.X"}' # intended result of the parsed_data
json_obj = json.loads(parsed_data)  # convert to json object
print(json_obj['system'])  # get a particular configuration information
print(json.dumps(json_obj, indent=4))  # , file=g)

json_obj['system'] = json.loads(
    '{"id":1, "name":"Mr.X"}')  # complexify/update the data
# it append not overrite the content of the file
json.dump(json_obj, g, indent=8)
g.close()

# sys.exit()
try:
    with open('result.out', 'r') as g:
        print(json.load(g))  # save as a file
except json.decoder.JSONDecodeError as e:
    print(dir(e))
    print(e)
    print(e.msg)
