import SendEmail_pb2 as SendEmail

send_email = SendEmail.SendEmail()
send_email.to = 'zxc'

with open("./serializedFile", "wb") as fd:
    fd.write(send_email.SerializeToString())
    print(send_email.SerializeToString())


send_email = SendEmail.SendEmail()
with open("./serializedFile", "rb") as fd:
    send_email.ParseFromString(fd.read())

print(send_email)
