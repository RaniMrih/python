import subprocess

#--------------------------------------------------------------------------------------------
#without text=true use decode, returncode = 0 
p1 = subprocess.run(['ls' , '-la'], capture_output=True)
print(p1.stdout.decode())
print(p1.returncode)

#--------------------------------------------------------------------------------------------
#with text=true use stdout
p1 = subprocess.run(['ls' , '-la'], capture_output=True , text=True)
print(p1.stdout())

#--------------------------------------------------------------------------------------------
#without capture_output use subrocess.PIPE
p1 = subprocess.run(['ls' , '-la'], stdout=subprocess.PIPE , text=True)
print(p1.stdout())

#--------------------------------------------------------------------------------------------
#without file
with open('output.txt' , 'w') as f:
    p1 = subprocess.run(['ls' , '-la'], stdout= f , text=True)

#--------------------------------------------------------------------------------------------
#python dont throu exeption test not exists
p1 = subprocess.run(['ls' , '-la' , 'test'], capture_output=True , text=True)
#check the error
print(p1.stderr)

#check returncode = 1 with error 
print(p1.returncode)

#can add conditions
# if p1.returncode != 0 : or if p1.returncode == 0

#--------------------------------------------------------------------------------------------
#python throu exeption if command failes add check=True
p1 = subprocess.run(['ls' , '-la' , 'test'], capture_output=True , text=True , check=True)
#check the error
print(p1.stderr)

#--------------------------------------------------------------------------------------------
#to ignore errors add DEVNULL returns None
p1 = subprocess.run(['ls' , '-la' , 'test'], stderr=subprocess.DEVNULL)
#check the error
print(p1.stderr)

#--------------------------------------------------------------------------------------------
#take first command output to be used as input to second command
p1 = subprocess.run(['cat' , 'text.txt'], capture_output=True, text=True)
print(p1.stdout)

#grep -n to show line number searching for the word text
p2 = subprocess.run(['grep' , '-n' , 'test'], capture_output=True, text=True, input=p1.stdout)
print(p1.stdout)

#using shell=True no need to pass arguments as list only as stringz
p1= subprocess.run('cat test.txt | grep -n test', capture_output=True, text=True, shell=True)
print(p1.stdout)





