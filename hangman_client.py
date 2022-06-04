import sys
from socket import *

HOST, PORT= sys.argv[1], int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST,PORT))

# Ask if user is ready to start the game
ready_ans = input('>>>Ready to start the game? (y/n): ')

# Reformat the user's answer and if it is not a y (or Y) then close the socket
if ready_ans != 'y':
    clientSocket.close()
# If user ready to play, then send an empty packet with msg_flag set to 0 to signal to the server to send an
# encoded word
else:
    msg = "0 "
    clientSocket.send(msg.encode())
    
while True:
    server_msg = clientSocket.recv(128)
    answer = server_msg.decode()

    flag = answer[0]
    
    if(flag=="0"):
        #flag | word_length | num_incorrect_guesses | data
        word_length = answer[1]
        num_incorrect_guesses = int(answer[2])
        guessing_word = answer[3:len(answer)-num_incorrect_guesses]
        incorrect_letter = answer[len(answer)-num_incorrect_guesses:]
        print(">>>"+guessing_word)
        print(">>>Incorrect Guesses:" +incorrect_letter)
        valid_input = False
        user_input = None
        while valid_input == False:
            user_input = input('>>>Letter to guess: ')
            if len(user_input) > 1 or not user_input.isalpha():
                print(">>>Error! Please guess one letter.\n")
            else:
                 
                valid_input = True
                msg = "1" + user_input
                clientSocket.send(msg.encode())              
    else:
        #flag | data
        for i in range (len(answer)):
            if(not answer[i].isnumeric()):
                print(">>>"+answer[i:])
                break
        break