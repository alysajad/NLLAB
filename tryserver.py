import socket

def encrypt():
    rail=[['\n' for _ in range (len(text))]for _ in range (key)]
    dir_down=False
    rows,cols=0,0
    for ch in text:
        if row==0 or row==key-1:
            dir_down=not dir_down
        rail[row][col]=ch
        col+=1
        row+=1 if dir_down else -1
        result=""

        for i in range (key):
            for j in range (len(text)):
                if rail[i][j]!='\n':
                    result+=rail[i][j]
        return result
    

