import base64

with open('token.pickle', 'rb') as f:
    token_pickle_content = f.read()
    token_pickle_base64 = base64.b64encode(token_pickle_content).decode('utf-8')

print(token_pickle_base64)
