import re


with open('data/RC_2006-02.txt', 'r') as f:
    text = f.readlines()
    text = '\n'.join(text)
    comments = re.findall(r'\"body\":\".*?\",\"', text)
    comments = '\n'.join(comments)
    comments = re.sub(r'\"body\":\"', '', comments)
    comments = re.sub(r'\"', '', comments)
    comments = re.sub(r'\[deleted\]', '', comments)
    comments = re.sub(r'\\n', '', comments)
    comments = re.sub(r'\\r', '', comments)


with open('data/reddit_comments.txt', 'w') as f:
    f.write(comments)
