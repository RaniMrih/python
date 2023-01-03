#Global VARIABLES
class Globals:
    def __init__ (self, TC, init_step , Config ,Doc_Name):
#        print "TC from Globals =" + str(TC)
#        print "init_step from Globals =" + str (init_step)
        self.EQ_Path='/usr/g/ctuser/EQ_Automation'
        self.Doc_Name= Doc_Name
        self.Output_Directory = self.EQ_Path+'/'+Doc_Name+'/'+TC+'/Outputfiles'
        self.TC_WD=self.EQ_Path+"/"+Doc_Name+ "/" + TC
        self.INITIAL_STEP = init_step
        self.Config = Config
        sinos_files = []
        lists_files = []
        Sinos_path=""
        Lists_path=""
