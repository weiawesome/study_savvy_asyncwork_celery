import time
import openai
def split_content(mode,content,size=2500):
    if(mode=='ASR'):
        content = [content[i:i + 2500] + '\n錄音未結束' for i in range(0, len(content), size)]
        content[-1] = content[-1][:-5] + '錄音結束'
    if(mode=='OCR'):
        if(len(content)>size):
            content = [content[i:i + 2500] + '\n作文未結束' for i in range(0, len(content), 2500)]
            content[-1] = content[-1][:-5] + '作文結束'
        else:
            content=[content]
    return content
def get_default_prompt(mode,prompt):
    if(mode=='ASR'):
        default_ASR_prompt = '現在你是專業的講師，你很會整理文章內重要訊息，並分析哪些會是重要考題，當內容提及考試內容或時間時請特別注意 幫我標註 並回答我，下面會給你上課錄音的轉錄內容聽完整份內容再回應'
        if len(prompt)!=0:
            default_ASR_prompt+="此堂課主題為:"+prompt+" 請特別注意此項領域 並且盡可能給予相關知識"
        return default_ASR_prompt
    if(mode=='OCR'):
        default_OCR_prompt = """你現在是學測英文作文的閱卷委員，請依照下面的評分準則，評分考生在內容、組織、文法句構、字彙拼字之表現，各項得分加總後給予一個整體分數(holistic score)，再依總分1至20分，分為下述五等級:特優(19-20分)、優(15-18分)、可 (10-14分)、差(5-9分)、劣(0-4分)。你在仔細評閱考生的作答內容後，再依其內容是否切題、組織是否具連貫性、句子結構與文法、用字是否適切表達文意，及拼字與標點符號使用是否正確等要項，進行評分。並且，字數不足120字者，扣總分1分;未分段者，亦扣總分1分。
評分準則:
    1.內容
        主題(句)清楚切題，並有具體、完整的相關細節支持。(5-4分)
        主題不夠清楚或突顯，部分相關敘述發展不全。(3分)
        主題不明，大部分相關敘述發展不全或與主題無關。(2-1分)
        文不對題或沒寫(凡文不對題或沒寫者，其他各項均以零分計算)。(0分)
    2.組織
        重點分明，有開頭、發展、結尾，前後連貫，轉承語使用得當。(5-4分)
        重點安排不妥，前後發展比例與轉承語使用欠妥。(3分)
        重點不明、前後不連貫。(2-1分)
        全文毫無組織或未按提示寫作。(0分)
    3.文法、句構
        全文幾無文法、格式、標點錯誤，文句結構富變化。(5-4分)
        文法、格式、標點錯誤少，且未影響文意之表達。(3分)
        文法、格式、標點錯誤多，且明顯影響文意之表達。(2-1分)
        全文文法錯誤嚴重，導致文意不明。(0分)
    4.字彙、拼字
        用字精確、得宜，且幾無拼字、大小寫錯誤。(5-4分)
        字詞單調、重複，用字偶有不當，少許拼字、大小寫錯誤，但不影響文意之表達。(3分)
        用字、拼字、大小寫錯誤多，明顯影響文意之表達。(2-1分)
        只寫出或抄襲與題意有關的零碎字詞。(0分)
評分後，請附上細節的建議，讓考生的英文作文可以達到更好的分數。
在建議的最後，附上簡短的鼓勵，讓考生知道我們很樂意幫忙。
"""
        if len(prompt)!=0:
            default_OCR_prompt+="\n此作文題目為:"+prompt+" 請特別注意此項領域 並且盡可能給予相關評論與修改方向"
        default_OCR_prompt+="\n作文內容如下:\n"
        return default_OCR_prompt
def get_default_details_prompt(mode):
    if(mode=='ASR'):
        default_ASR_prompt = {'重要觀念:':'根據以上所有內容做出整理 整理出重要的觀念','可能考題方向:':'根據以上所有內容做出整理 整理出考題方向','考試時間與範圍:':'根據以上所有內容做出整理 老師是否提出下次要考試 若要考試給出考試時間與範圍'}
        return default_ASR_prompt
    if(mode=='OCR'):
        default_OCR_prompt = {'評分':'根據提供的rubric 在1至20分的分數範圍內 評分考生的英文作文', '細節的建議':'根據提供的rubric 提出可使考生獲得更高分的建議', '簡短的鼓勵':'給考生正向的鼓勵'}
        return default_OCR_prompt

def combine_results(results):
    result=''
    for i in results.keys():
        result+=i+'\n'+results[i]+'\n\n'
    return result
def combine_message(messages,results):
    message=messages
    for i in results.keys():
        message.append(results[i])
    return message

def continue_Chat(chatbot,prompt):
    result=''
    extra=''
    for data in chatbot.ask(prompt, ):
        result = data["message"]
    while (data['end_turn'] != True):
        for data in chatbot.continue_write():
            extra = data["message"]
        result += extra
        time.sleep(5)
    return result

def openai_continue_Chat(reqs):
    result=''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=reqs
    )
    response = response.to_dict()
    reqs.append(reqs, response['choices'][0]['message'])
    result+=response['choices'][0]['message']['content']
    while (response['choices'][0]['finish_reason'] != 'stop'):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=reqs
        )
        response = response.to_dict()
        reqs.append(reqs, response['choices'][0]['message'])
        result += response['choices'][0]['message']['content']
        time.sleep(1)
    return reqs,result
def openai_add_prompt(reqs,content):
    reqs.append({'role':'user','content':content})
    return reqs