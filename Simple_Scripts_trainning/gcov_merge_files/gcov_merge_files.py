#!/bin/python
import sys
import argparse
#---------------------------------------------------
#Formola:
#not covered + not executable = not covered
#covered + not executable or not covered = covered 
#covered + covered = covered
#---------------------------------------------------

####################### functions ##########################
# parse input output
def parse_arguments (args):
    list_params = ["input", "output"]
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--input",     action='store', nargs=1, help="")
    parser.add_argument("--output",    action='store', nargs=1, help="")
    args_array = parser.parse_args(args[1:])
    for param in list_params:
        if (args_array.__getattribute__(param)):
            args_array.__setattr__(param, args_array.__getattribute__(param)[0])
    return args_array

#---------def 2 files merge support ------------
def merge_two_files(file1,file2,outfile):
    List1 = file1.readlines()
    List2 = file2.readlines()
    Length = len(List1)

    with open(outfile, 'w') as results:
        for i in range (Length):
            file1_str = List1[i]
            file2_str = List2[i]
            #include first 10 lines of all files

            if i < 9:
              results.writelines(file1_str)
              results.writelines(file2_str)
            else:
                #check if line starts with number
                if List1[i].lstrip()[:1].isdigit() or List2[i].lstrip()[:1].isdigit():
                   if List1[i].lstrip()[:1].isdigit():
                      results.writelines(file1_str)
                   else:
                      results.writelines(file2_str)

                #check if line starts with "#"             
                elif List1[i].lstrip().startswith("#") or List2[i].lstrip().startswith("#"):
                    if List1[i].lstrip()[:1].startswith("#"):
                       results.writelines(file1_str)
                    else :
                       results.writelines(file2_str)
                # if line starts with "-:" 
                else:
                    results.writelines(file1_str)

#---------def 3 files merge support ------------
def merge_three_files(file1,file2,file3,outfile):
    List1 = file1.readlines()
    List2 = file2.readlines()
    List3 = file3.readlines()
    Length = len(List1)

    with open(outfile, 'w') as results:
        for i in range (Length):
            file1_str = List1[i]
            file2_str = List2[i]
            file3_str = List3[i]
            #include first 10 lines of all files

            if i < 9:
              results.writelines(file1_str)
              results.writelines(file2_str)
              results.writelines(file3_str)

            else:
                #check if line starts with number
                if List1[i].lstrip()[:1].isdigit() or List2[i].lstrip()[:1].isdigit() or List3[i].lstrip()[:1].isdigit():
                   if List1[i].lstrip()[:1].isdigit():
                      results.writelines(file1_str)
                   elif List2[i].lstrip()[:1].isdigit():
                      results.writelines(file2_str)
                   else:
                      results.writelines(file3_str)

                #check if line starts with "#"             
                elif List1[i].lstrip().startswith("#") or List2[i].lstrip().startswith("#") or List3[i].lstrip().startswith("#"):
                    if List1[i].lstrip()[:1].startswith("#"):
                       results.writelines(file1_str)
                    elif List2[i].lstrip()[:1].startswith("#"):
                        results.writelines(file2_str)
                    else :
                       results.writelines(file3_str)
                # if line starts with "-:" 
                else:
                    results.writelines(file1_str)

############################ main ##########################
if __name__ =="__main__":
    args_array = parse_arguments(sys.argv)

    #check --input --output arrgs
    if args_array.input == "" or args_array.output == "" or args_array.input == None or args_array.output == None :
        print("Error, plese run the script inserting vaild --input 'file1 file2 file3' and --output 'output_file.txt'")

    else:
        #split inputs check how many files inserted
        user_files = args_array.input.split()
        outfile = str(args_array.output)
        file1 = open(str(user_files[0]), "r")
        file2 = open(str(user_files[1]), "r")

        if len(user_files) == 2:
            merge_two_files(file1,file2,outfile)

        if len(user_files) == 3:
            file3 = open(str(user_files[2]), "r")
            merge_three_files(file1,file2,file3,outfile)
        print("Success, output file is " + str(args_array.output))