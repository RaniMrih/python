#this program calculates the volume of cylinder given RADIUS and Height
import math
import argparse

#creating the parser to store arguments
parser = argparse.ArgumentParser(description="Calculate volume of cylinder")
parser.add_argument('-r','--radius',type=int,metavar='',required=True ,help="Radius of cylinder")
parser.add_argument('-H','--height',type=int,metavar='',required=True, help="Height of cylinder")
#creating group for displaying output in diffrent ways
group = parser.add_mutually_exclusive_group()
group.add_argument('-q','--quiet',action='store_true',help='Print quiet output')
group.add_argument('-v','--verbose',action='store_true',help='Print verbose output')
#parsing the args
args=parser.parse_args()

def cylinder_volume(radius,height):
    vol = (math.pi) * (radius**2) * (height)
    return vol

if __name__ == "__main__":
    volume = cylinder_volume(args.radius,args.height)
    if args.quiet:
        print(volume)
    elif args.verbose:
        print('Volume of Cylinder with radius of %s and height %s is : %s' % (args.radius, args.height, volume))
    else:
        print('Volume of Cylinder is %s'%(volume))   

# expected output:
# -----------------
# PS C:\Users\rmrih\Rani_GitHub\python\Simple_Scripts_trainning> .\Arguments_parse.py -r 2 -H 4
# Volume of Cylinder is 50.26548245743669
# PS C:\Users\rmrih\Rani_GitHub\python\Simple_Scripts_trainning> .\Arguments_parse.py -r 2 -H 4 -v
# Volume of Cylinder with radius of 2 and height 4 is : 50.26548245743669
# PS C:\Users\rmrih\Rani_GitHub\python\Simple_Scripts_trainning> .\Arguments_parse.py -r 2 -H 4 -q
# 50.26548245743669
# PS C:\Users\rmrih\Rani_GitHub\python\Simple_Scripts_trainning>  