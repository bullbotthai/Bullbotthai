import pprint
from flask import Flask , request
# from{ name of your file } import search
from wolf import search_wiki
##การเข้าไฟล์ผ่านโฟลเดอร์ from folder.filename import function
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':

        pp = pprint.PrettyPrinter(indent=3)
        ### dictionary from line
        data = request.json
        data_show = pp.pprint(data)

        ## extract text from line
        text_fromline = data['events'][0]['message']['text']
        ## ค้นหาคำจาก wikipedia
        result = search_wiki(text_fromline)

        ### import function ในการส่งmessage reply.py
        from reply import ReplyMessage

        ReplyMessage(Reply_token=data['events'][0]['replyToken'],
        TextMessage=result,
        Line_Access_Token='SUoCA5pwOPSQ0LRMR2zuGeZTbg3nJtQJEGKVpTSTFJsgwuWfP6qPB06Pp179ar9lJayy6lvBaZBvqD+Ynx/sJqlzXo/4v0c6EMt7hsSWHCy1Q54vdjkfGb/ufXQi1bGPczfWuCLZPOe5jiette9uZwdB04t89/1O/w1cDnyilFU='
        )


        return 'OK'

    elif request.method == 'GET':
        return 'นี้คือลิงค์เว็บสำหรับรับ package'

if __name__ == "__main__":
    app.run(port=200)
