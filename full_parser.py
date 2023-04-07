# Simple JSON parser in Python taken from https://github.com/eatonphil/pj

JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'
JSON_QUOTE = '"'
JSON_QUOTE = '"'
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')

def lex_string(string):
    json_string = ''

    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    for c in string:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += c

    raise Exception('Expected end-of-string quote')


def lex_number(string):
    json_number = ''

    number_characters = [str(d) for d in range(0, 10)] + ['-', 'e', '.']

    for c in string:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def lex_bool(string):
    string_len = len(string)

    if string_len >= TRUE_LEN and \
         string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and \
         string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string


def lex_null(string):
    string_len = len(string)

    if string_len >= NULL_LEN and \
         string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]

    return None, string


def lex(string):
    tokens = []

    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        c = string[0]

        if c in JSON_WHITESPACE:
            # Ignore whitespace
            string = string[1:]
        elif c in JSON_SYNTAX:
            tokens.append(c)
            string = string[1:]
        else:
            raise Exception('Unexpected character: {}'.format(c))

    return tokens

def parse_array(tokens):
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]

    raise Exception('Expected end-of-array bracket')


def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected string key, got: {}'.format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(t))

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))

        tokens = tokens[1:]

    raise Exception('Expected end-of-object bracket')

def parse(tokens, is_root=False):
    t = tokens[0]

    if is_root and t != JSON_LEFTBRACE:
        raise Exception('Root must be an object')

    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


# JSON string
json_str = '''
{
    "instructions": [
        {"command": "move", "direction": "forward", "distance": 50},
        {"command": "turn", "direction": "right", "angle": 90},
        {"command": "move", "direction": "backward", "distance": 30},
        {"command": "turn", "direction": "left", "angle": 45},
        {"command": "move", "direction": "forward", "distance": 20},
        {"command": "turn", "direction": "right", "angle": 180},
        {"command": "move", "direction": "forward", "distance": 70},
        {"command": "turn", "direction": "left", "angle": 90}
    ]
}
'''

# Convert JSON string to a list of tokens
tokens = lex(json_str)

# Parse the tokens and convert them to a Python object
obj, _ = parse(tokens, is_root=True)

# Print the Python object
print(obj)

# Print out each key-value pair in the obj['instructions'] list
for instruction in obj['instructions']:
    for key, value in instruction.items():
        # print(key, value)
        if value == 'move':
            direction = instruction['direction']
            distance = instruction['distance'] 
            if direction == 'forward': 
                chassis_ctrl.move_with_distance(0, distance)
            elif direction == 'right': 
                chassis_ctrl.move_with_distance(90, distance)
            elif direction == 'backward': 
                chassis_ctrl.move_with_distance(180, distance)
            else:
                chassis_ctrl.move_with_distance(-90, distance)
            print(f'Move params: {direction, distance}')   
        elif value == 'turn':
            direction = instruction['direction']
            angle = instruction['angle']  
            chassis_ctrl.rotate_with_degree(direction, angle)
            print(f'Turn params: {direction, angle}')    
