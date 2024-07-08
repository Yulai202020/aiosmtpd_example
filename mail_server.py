import asyncio, os, json, sqlite3
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
from email.message import EmailMessage
from datetime import datetime

class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        sender = envelope.mail_from
        recipients = envelope.rcpt_tos
        content = envelope.content.decode('utf8', errors='replace')

        # get time
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H:%M:%S.%f") +".json"

        # split by new line
        splited_mes = content.split("\n")
        index = splited_mes.index("\r")

        # get body and headers
        body = splited_mes[index+1:]
        headers = splited_mes[:index]

        # split headers to dictinary
        split_headers = {}

        for i in headers:
            id_ = i.find(": ")
            if id_ != -1:
                split_headers[i[:id_]] = i[id_+2:-1]

        # 
        new_body = []
        for i in body:
            if len(i) > 0:
                i= i[:-1]
                new_body.append(i)
        
        new_body = "\n".join(new_body)

        # add body
        split_headers["body"] = new_body

        # write to file
        string = json.dumps(split_headers, indent=2)
        with open(f"mails/{filename}", "w") as f:
            f.write(string)
        
        with sqlite3.connect('my.db') as conn:
            sql = f'''INSERT INTO Headers(subject, from_, to_, body) VALUES("{split_headers["Subject"]}", "{split_headers["From"]}", "{split_headers["To"]}", "{split_headers["body"]}");'''
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

        # send answer
        response = "ok probably"
        return f"250 {response}"

if __name__ == "__main__":
    handler = EmailHandler()
    controller = Controller(handler, hostname='localhost', port=8025)
    controller.start()

    print("SMTP server is running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.stop()
        print("SMTP server stopped.")
