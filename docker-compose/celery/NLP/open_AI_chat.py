import openai

from NLP.utils import get_default_prompt, split_content, openai_continue_Chat, openai_add_prompt, \
    get_default_details_prompt, combine_results, combine_message


def openaiChat(api_key,mode,prompt,text):

    prompt = get_default_prompt(mode,prompt)


    openai.api_key = api_key
    reqs = []
    text = split_content(mode,text)

    messages = []
    reqs=openai_add_prompt(reqs,prompt)
    reqs,result=openai_continue_Chat(reqs)
    messages.append(result)
    for i in range(len(text)):
        reqs=openai_add_prompt(reqs,'以下是內容\n'+text[i])
        reqs, result = openai_continue_Chat(reqs)
        messages.append(result)
    results = {}
    prompts = get_default_details_prompt(mode)
    for i in prompts.keys():
        reqs = openai_add_prompt(reqs, prompts[i])
        reqs, result = openai_continue_Chat(reqs)
        results[i] = result

    result = combine_results(results)
    message = combine_message(messages,results)

    return message, result

def openaiChat_test(api_key):
    try:
        openai.api_key = api_key
        reqs = []
        reqs = openai_add_prompt(reqs, 'hello')
        reqs, result = openai_continue_Chat(reqs)
    except:
        return False
    return True