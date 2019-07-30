import markovify
import json

# Get raw text as string.
with open("data/The-Fountainhead_dataset.txt") as f:
    f_text = f.read()

fountainhead = markovify.Text(f_text, state_size=3)

with open("data/the_catcher_in_the_rye.txt") as f:
    c_text = f.read()

catcher = markovify.Text(c_text, state_size=3)

'''
with open("data/data_from_OANC/merged-file.txt") as f:
    biomed_text = f.read()

biomed = markovify.Text(biomed_text, state_size=3)
'''

with open("data/letters_OANC/merged-file.txt") as f:
    letters_text = f.read()

letters = markovify.Text(letters_text, state_size=3)

with open("data/corp.txt") as f:
    corp_text = ''
    for line in f.readlines():
        if len(line) > 10:
            line = line[6:-5]
            corp_text += line

corp = markovify.Text(letters_text, state_size=3)

with open("data/reddit_comments.txt") as f:
    reddit_text = f.read()

reddit = markovify.Text(reddit_text, state_size=3)

text_model = markovify.combine([fountainhead, catcher, letters, reddit, corp], [1, 1, 1, 1, 0.1])

model_json = text_model.to_json()

with open('data.json', 'w') as f:
    json.dump(model_json, f)
