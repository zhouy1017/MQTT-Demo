
def handle(client,topic,payload,mem):
    topic_s = topic.split('/')
    if topic_s[2] == 'task1' and topic_s[3] == 'requests':
        return
    if topic_s[2] == 'task1' and topic_s[3] == 'responses':
    #print(mem)
        # identify operation
        id = int(payload[0:4])
        output = str(mem[id]) + ":::" + payload[4:]
        print(output)
    else:
        print("Command not supported yet!")
