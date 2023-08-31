from revChatGPT.V1 import Chatbot
from NLP.utils import split_content, get_default_prompt, get_default_details_prompt, combine_results, combine_message, \
    continue_Chat

def revChat(access_token,mode,prompt,text):

    prompt=get_default_prompt(mode,prompt)

    chatbot = Chatbot(config={
        "model": "gpt-3.5-mobile",
        "access_token": access_token
    })

    text = split_content(mode,text)

    messages = []
    messages.append(continue_Chat(chatbot, prompt))
    for i in range(len(text)):
        messages.append(continue_Chat(chatbot,'以下是內容\n'+text[i]))

    results={}
    prompts=get_default_details_prompt(mode)
    for i in prompts.keys():
        results[i]=continue_Chat(chatbot, prompts[i])


    result=combine_results(results)
    message=combine_message(messages,results)

    conv_id=chatbot.conversation_id
    chatbot.delete_conversation(conv_id)

    return message,result

def revChat_test(access_token):
    try:
        chatbot = Chatbot(config={"model":"gpt-3.5-mobile","access_token": access_token})
        continue_Chat(chatbot, 'hello')
        conv_id = chatbot.conversation_id
        chatbot.delete_conversation(conv_id)
        return True
    except:
        return False
