
import datetime
import sys, re, logging
from datetime import datetime
import socket
import datetime as my_datetime

PORT=8080
HOST="127.0.0.1"
  

def getHeader(connection):
    currentChunk = connection.recv(1)
    recievedMsg = currentChunk
    while currentChunk != '':
        currentChunk = connection.recv(1)
        recievedMsg = recievedMsg + currentChunk
        if "\r\n\r\n" in recievedMsg:
            break
    
    return recievedMsg

def getContentLenght(header):
    lines = header.split("\r\n")
    #print 'The lines are ', lines
    for line in lines:
        if "Content-Length:" in line:
            s = line.split(":")
            #print 'The content is ', s
            return int(s[1])
    return 0

def getBody(connection, contentLenght):
    return connection.recv(contentLenght)

    
def parse_request(request, connection):
    lines=request
    if len(lines)<1:
        return None
    words=lines.split()
    
    if len(words)<3:
        return None
    if words[0]=="GET" or words[0]=="POST" and words[2] in ["HTTP/1.0","HTTP/1.1"]:
        method = words[0]
        url = words[1]
        #print 'Method is ',method
        #print'Url is ', url
        if words[0]=="POST":
            #print 'post entered'
            contentLenght = getContentLenght(request)
            post_data = ""

            if contentLenght!= 0:

                data_line = getBody(connection, contentLenght)
                print "Data line", data_line
                exp =  r'(?P<key>.*?)=(?P<val>.*?)&'
                data_line += '&'     #Appending additional & at the end of the text to match with regular expression
                post_data_dict = dict(re.findall(exp,data_line))
                return (method, url, post_data_dict)
        
        else:
            return (method, url, [])
    else:
        return None    
    

def sendResponse(response, connection):
    connection.sendall(response)
    
def create_document(s):
    return "Content-Type: text/html;\n\r\n\r"+ \
           "<html><body>\n\r"+s+"</body></html>\n\r"
 
def create_response(status,s):
    return "HTTP/1.1 "+status+"\n\r"+ \
           s+"\n\r"


def is_it_friday(d):
    """First check to see if the user input can be converted to datetime object"""
    if not isinstance(d, my_datetime.date):
        try:
            d = datetime.strptime(d, '%d%m%Y')
        except Exception:
            return 'Your input seems invalid. Enter in format ddmmyyyy'

    if d.isoweekday()==5:
        return "Yes, it is Friday!"
    else:
        return "No, the date you entered is not friday."
    

def fetch_response(parameters):
    if parameters is None:
        return None
    else:
        return is_it_friday(parameters)
    return is_it_friday(datetime.now())

def fridayWebapp(connection):
    response = ""
    header = getHeader(connection)#gets all the content from client request
    parameters = parse_request(header, connection)
    #print parameters
    date_pattern = re.compile(r'/\d{8}')
    
    if parameters[1] == '/dateform' and parameters[0]=='GET':
        response = get_date_form()
        html_response = create_response(
            "200 OK",
            create_document(response)
            )

    elif re.match(date_pattern, parameters[1]):
        url_pattern = parameters[1].strip('/')
        #input_date = datetime.strptime(url_pattern, '%d%m%Y')
        response = fetch_response(url_pattern)
        html_response=create_response(
                "200 OK",
                create_document(response)
                )
    elif parameters[0] == 'POST':
        date_from_post = parameters[2]['date']
        password_from_post= parameters[2]['password']
        if password_from_post != '123':
            create_log_file(password_from_post)
            response="Your password is not correct and this info is logged"
        else:
            response = fetch_response(date_from_post)
        html_response=create_response(
            "200 Ok",
            create_document(response)
            )
    elif parameters[1] == '/log':
        html_response = get_file_content()
    else:
        html_response=create_response(
                "500 Error",
                "Invalid request"
                )        
    sendResponse(html_response, connection)

def server(handler, port=PORT, host=HOST, queue_size=5):
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.bind((host, port))
    mysocket.listen(queue_size)
    while True:
        print "Waiting at http://%s:%d" % (host, port)
        (connection, addr) = mysocket.accept()
        print "New connection", connection, addr
        handler(connection)
        connection.close()
        print "Connection closed."


def get_date_form():
    return '''
    <form method="POST">
        <p>Enter your date here <input type="text" name="date"></p>
        <p>Enter your password here <input type="password" name="password"></p>
        <input type="submit" value="submit">
    </form>
    '''


def create_log_file(password):
    with open('log.txt','a+') as f:
        f.write('%s user entered incorrect password: %s\n' %(str(datetime.now()), password))

def get_file_content():
    with open('log.txt','r') as f:
        file_data = f.read()
    return file_data
server(fridayWebapp)