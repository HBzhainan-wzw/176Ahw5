from socket import *
import threading
import time
import sys
import random
# sys.path.append(".")

num_incorrect_guesses = 0
inc_letters = []
word_dict = []
word = ""


def getSum(n):
    sum = 0
    for digit in str(n): 
      sum += int(digit)      
    return sum

def init_word():
    global word
    word = random.choice(word_dict)
    new_string = ""
    for i in range(len(word)):
        new_string += "_"
    return new_string    

def print_letters(list):
    letters = ""
    for i in list:
        letters += i
    return letters

def replace_letter(word1, word2, letter):
    word2 = list(word2)
    for i in range(len(word1)):
        if(word1[i] in letter):
            word2[i] = letter
    return ''.join(word2)

            
def function_name(connectionSocket,addr):    
    while True:
        client_msg = connectionSocket.recv(128).decode()
        client_msg_flag = client_msg[0]
        client_data = client_msg[1]
        #flag | word_length | num_incorrect_guesses | data
        
        global num_incorrect_guesses
        global inc_letters
        global word
        
        #starting package
        if client_msg_flag == "0":
            flag = "0"
            word_length = str(len(word))
            num_incorrect_guesses = 0
            modified_word = init_word()
            data = init_word()
            server_msg = flag+word_length+str(num_incorrect_guesses)+data
            connectionSocket.send(server_msg.encode())
        
        else:
            if(num_incorrect_guesses < 7):            
                flag = "0"
                word_length = str(len(word))
                
                if(client_data in word):
                    modified_word = replace_letter(word, modified_word, client_data)
                    #flag | data
                    if(modified_word == word):
                        data = "The word was " + word + "\n" +"You Win!\n" + "Game Over!"
                        flag = str(len(data))
                        server_msg = flag+data
                        connectionSocket.send(server_msg.encode())
                        break
                        
                        
                else:
                    if(client_data not in inc_letters):
                        inc_letters.append(client_data)
                    num_incorrect_guesses += 1
                
                data = modified_word
                                
                num_incorrect_guesses = len(inc_letters)
                
                data = data+print_letters(inc_letters)
                server_msg = flag+word_length+str(num_incorrect_guesses)+data
                connectionSocket.send(server_msg.encode())            
            else:
                        data = "The word was " + word + "\n" +"You Lose:(\n" + "Game Over!"
                        flag = len(data)
                        server_msg = flag+data
                        connectionSocket.send(server_msg.encode())
                        break
                
if __name__=="__main__":
    serverPort = int(sys.argv[1])
    seed = int(sys.argv[2])
    random.seed(seed)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    # count thread number
    threadCnt = 0
    f = open('hangman_words.txt')
    content_list = []
    word_dict = []
    for line in f:
        content_list.append(line.strip('\n'))
    content_list[:] = [i for i in content_list if i != '']
    for i in range(0,len(content_list)):
        word_dict.append(content_list[i])
  
    while True:
        serverSocket.listen()
        if(threadCnt > 2):
            print("server-overloaded")
            continue
        try:
            connectionSocket, addr = serverSocket.accept()
            threading.Thread(target=function_name,args=(connectionSocket,addr)).start()
            threadCnt += 1
        except:
            print('')

        
    