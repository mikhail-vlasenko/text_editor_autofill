import markovify

# Get raw text as string.
with open("data/The-Fountainhead_dataset.txt") as f:
    text = f.read()

text_model = markovify.Text(text, state_size=3)


def get_cont(sent, max_w_cont, num_tries=10, max_coef=0.1, silent=True):
    res = None
    cnt = 0
    sep = ' '
    while not res:
        if cnt > num_tries:
            res = text_model.make_sentence_with_start(beginning=sent, max_words=len(sent.split()) +
                                                                                int(max_w_cont * max_coef * (
                                                                                            cnt - num_tries)))
            if res:
                if not silent:
                    print(res)
                    print("lenght = " + str(len(res.split())))
                    print("cnt = " + str(cnt))
                res = sep.join(res.split()[:len(sent.split()) + max_w_cont])
        else:
            res = text_model.make_sentence_with_start(beginning=sent, max_words=len(sent.split()) + max_w_cont)
        cnt += 1
    return res
