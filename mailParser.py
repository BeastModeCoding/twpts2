import os
import imaplib
import email
import time
from email.header import decode_header
from html.parser import HTMLParser

password = os.getenv('AppPassword')
sender = "Twitch <account@twitch.tv>"
code = 0

class MyHTMLParser(HTMLParser):
	
	def handle_data(self, data):
		if data[0:6].isdigit():
			global code
			code = data[0:6]
# 			print(f"Code is {code}")
			
parser = MyHTMLParser()

def getFrickingCode():
	time.sleep(4)
	with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
		print("Connection Object : {}".format(imap_ssl))
		
		############### Login to Mailbox ######################
		print("Logging into mailbox...")
		resp_code, response = imap_ssl.login("xxxredsn0wxxx@gmail.com", password)
		
		print("Response Code : {}".format(resp_code))
		print("Response      : {}\n".format(response[0].decode()))
		
		############### Set Mailbox #############
		resp_code, mail_count = imap_ssl.select(mailbox="inbox", readonly=True)
		
		############### Search mails in a given Directory #############   
		resp_code, mails = imap_ssl.search(None, 'ALL')
		mail_ids = mails[0].decode().split()
		print("Total Mail IDs : {}\n".format(len(mail_ids)))
		
		# for mail_id in mail_ids[-1:]:
		# 	print("================== Start of Mail [{}] ====================".format(mail_id))
		# 	resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)') ## Fetch mail data.
		# 	message = email.message_from_bytes(mail_data[0][1]) ## Construct Message from mail data
		# 	# message = base64.b64decode(mail_data).decode("UTF-8")
		# 	print("From       : {}".format(message.get("From")))
		# 	print("To         : {}".format(message.get("To")))
		# 	print("Bcc        : {}".format(message.get("Bcc")))
		# 	print("Date       : {}".format(message.get("Date")))
		# 	print("Subject    : {}".format(message.get("Subject")))
		# 	print("Body : ")
		# 	for part in message.walk():
		# 		if part.get_content_type() == "text/plain":
		# 			body_lines = part.as_string().split("\n")
		# 			print("\n".join(body_lines)) ### Print first few lines of message
		# 	print("================== End of Mail [{}] ====================\n".format(mail_id))
	
		N = 1
		for mail_id in mail_ids[-N:]:
			print("================== Start of Mail [{}] ====================".format(mail_id))
			# fetch the email message by ID
			res, msg = imap_ssl.fetch(str(mail_id), "(RFC822)")
			for response in msg:
				if isinstance(response, tuple):
					# parse a bytes email into a message object
					msg = email.message_from_bytes(response[1])
					# decode the email subject
					subject, encoding = decode_header(msg["Subject"])[0]
					if isinstance(subject, bytes):
						# if it's a bytes, decode to str
						subject = subject.decode(encoding)
					# decode email sender
					From, encoding = decode_header(msg.get("From"))[0]
					if isinstance(From, bytes):
						From = From.decode(encoding)
					print(f"Subject    : {subject}")
					print(f"From       : {From}")
					if From == sender:
						print("Matched")
						# if the email message is multipart
						if msg.is_multipart():
						# iterate over email parts
							for part in msg.walk():
						# extract content type of email
								content_type = part.get_content_type()
								content_disposition = str(part.get("Content-Disposition"))
								try:
								# get the email body
									body = part.get_payload(decode=True).decode()
								except:
									pass
								if content_type == "text/plain" and "attachment" not in content_disposition:
								# print text/plain emails and skip attachments
									print(body)
						else:
		# extract content type of email
							content_type = msg.get_content_type()
		# get the email body
							body = msg.get_payload(decode=True).decode()
							if content_type == "text/plain":
		# print only text email parts
								print(body)
						if content_type == "text/html":
							parser.feed(body)
			print("================== End of Mail [{}] ====================\n".format(mail_id))					
		############# Close Selected Mailbox #######################
		print("\nClosing selected mailbox....")
		imap_ssl.close()
	return code

if __name__ == "__main__":
  code = getFrickingCode()
