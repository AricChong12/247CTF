#!/usr/bin/env python3
from pwn import *

# Important: the service expects \r\n, not just \n
context.newline = b'\r\n'
context.log_level = 'error'   # change to 'info' or 'debug' if you want more output

HOST = 'ec4234a270ce177e.247ctf.com'
PORT = 50045

r = remote(HOST, PORT)

# Skip the two welcome lines
r.recvline()
r.recvline()

for i in range(500):
    problem = r.recvline().decode().strip()
    # Example: "What is the answer to 380 + 213?"
    parts = problem.split()
    a = int(parts[5])
    b = int(parts[7].rstrip('?'))
    
    answer = str(a + b)
    r.sendline(answer)
    
    # Consume the "Yes, correct!" line
    r.recvline()
    
    if (i + 1) % 100 == 0:
        print(f"Solved {i + 1}/500")

# After 500 correct answers the flag is sent
flag = r.recvline().decode().strip()
print(flag)

r.close()