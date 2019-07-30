import markovify
import json

with open('data.json', 'r') as f:
    json_model = json.load(f)

text_model = markovify.Text.from_json(json_model)


def get_cont(sent, max_w_cont, num_tries=10, max_coef=0.1, max_tries=10, silent=True, strict=True):
    res = None
    cnt = 0
    sep = ' '
    while not res:
        if cnt > num_tries:
            res = text_model.make_sentence_with_start(beginning=sent,
                                                      max_words=len(sent.split()) + int(max_w_cont * max_coef * (cnt - num_tries)),
                                                      strict=strict)
            if res:
                if not silent:
                    print(res)
                    print("lenght = " + str(len(res.split())))
                    print("cnt = " + str(cnt))
                res = sep.join(res.split()[:len(sent.split()) + max_w_cont])
            elif cnt >= max_tries:
                print('Ran out of tries')
                return -1
        else:
            try:
                res = text_model.make_sentence_with_start(beginning=sent,
                                                          max_words=len(sent.split()) + max_w_cont,
                                                          strict=strict)
            except KeyError:
                print('Can\'t continue')
                return -1
        cnt += 1
    return res
