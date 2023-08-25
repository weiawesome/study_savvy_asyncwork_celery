from transformers import AutoTokenizer, AutoModel

from NLP.utils import get_default_prompt, split_content, get_default_details_prompt, combine_results, combine_message


def glmChat(mode,prompt,text):

    prompt = get_default_prompt(mode,prompt)

    revision = "main"
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True, revision=revision)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True, revision=revision).half().cuda()

    text = split_content(mode,text,size=500)

    messages = []
    response, history = model.chat(tokenizer, prompt,history=[])
    messages.append(response)
    for i in range(len(text)):
        response, _ = model.chat(tokenizer, '以下是內容\n'+text[i],history=history)
        messages.append(response)

    results = {}
    if(len(text)==1):
        prompts = get_default_details_prompt(mode)
        for i in prompts.keys():
            response, __ = model.chat(tokenizer, prompts[i], history=_)
            results[i]=response
        result = combine_results(results)
        message = combine_message(messages,results)
    else:
        result='抱歉個人模型目前無法處理過長資訊'

    return message, result