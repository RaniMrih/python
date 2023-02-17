from __future__ import print_function

import sys
import simplejson as json
def json_build(res_dct,image,string):


    prep = image.split(":")
    #print "kkkk",prep
    if len(prep) == 1:
        string.append(json.dumps({'image':prep[0],'size':res_dct[prep[0]]['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':res_dct[prep[0]]['customizations'][0]}))
    if len(prep) == 2:
        if prep[1] in res_dct[prep[0]]['modifiers']:
            string.append(json.dumps({'image':prep[0],'size':res_dct[prep[0]]['size'],'mod':prep[1],'custom':res_dct[prep[0]]['customizations'][0]}))
        elif prep[1] in res_dct[prep[0]]['customizations']:
            string.append(json.dumps({'image':prep[0],'size':res_dct[prep[0]]['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':prep[1]}))
        else:
            try:
                if int(prep[1]):
                    string.append(json.dumps({'image':prep[0],'size':prep[1],'mod':res_dct[prep[0]]['modifiers'][0],'custom':res_dct[prep[0]]['customizations'][0]}))

            except ValueError:
                print('1')
                try:
                    if float(prep[1]):
                        string.append(json.dumps({'image':prep[0],'size':prep[1],'mod':res_dct[prep[0]]['modifiers'][0],'custom':res_dct[prep[0]]['customizations'][0]}))
                except ValueError:
                    print("Wrong value: %s, should be number\n\nRegards ItDevOps" % prep[1])
                    sys.exit(2)

    if len(prep) == 3:
        if prep[1] not in res_dct[prep[0]]['modifiers'] and not prep[1] in res_dct[prep[0]]['customizations']:
            try:
                size_int = {}
                if int(prep[1]):
                    size_int['size'] = prep[1]
                    if prep[2] in res_dct[prep[0]]['modifiers']:
                        string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':prep[2],'custom':res_dct[prep[0]]['customizations'][0]}))
                    if prep[2] in res_dct[prep[0]]['customizations']:
                        string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':prep[2]}))


            except ValueError:
                print('i12')
                try:
                    if float(prep[1]):
                        size_int['size'] = prep[1]
                        if prep[1] in res_dct[prep[0]]['modifiers']:
                            string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':prep[1],'custom':res_dct[prep[0]]['customizations'][0]}))
                        if prep[1] in res_dct[prep[0]]['customizations']:
                            string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':prep[1]}))
                except ValueError:
                    print('22')
                    print("Wrong value: %s, should be number\n\nRegards ItDevOps" % prep[1])
                    sys.exit(2)

        if prep[1] in res_dct[prep[0]]['modifiers'] and prep[2] in res_dct[prep[0]]['customizations']:
            string.append(json.dumps({'image':prep[0],'size':res_dct[prep[0]]['size'],'mod':prep[1],'custom':prep[2]}))
        if prep[1] in res_dct[prep[0]]['customizations'] and prep[2] in res_dct[prep[0]]['modifiers'] :
            string.append(json.dumps({'image':prep[0],'size':res_dct[prep[0]]['size'],'mod':prep[2],'custom':prep[1]}))
        else:
            try:
                size_int = {}
                if int(prep[2]):
                    size_int['size'] = prep[2]
                    if prep[1] in res_dct[prep[0]]['modifiers']:
                        string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':prep[1],'custom':res_dct[prep[0]]['customizations'][0]}))
                    if prep[1] in res_dct[prep[0]]['customizations']:
                        string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':prep[1]}))


            except ValueError:
                print('442')
                try:
                    if float(prep[1]):
                        size_int['size'] = prep[1]
                        if prep[1] in res_dct[prep[0]]['modifiers']:
                            string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':prep[1],'custom':res_dct[prep[0]]['customizations'][0]}))
                        if prep[1] in res_dct[prep[0]]['customizations']:
                            string.append(json.dumps({'image':prep[0],'size':size_int['size'],'mod':res_dct[prep[0]]['modifiers'][0],'custom':prep[1]}))
                except ValueError:
                    print('4423')
                    print("Wrong value: %s, should be number\n\nRegards ItDevOps" % prep[1])
                    sys.exit(2)




    if len(prep) == 4:
        #print res_dct
        if prep[1] in res_dct[prep[0]]['modifiers']:
            #print "mod0",prep[1]
            mod = prep[1]
        if prep[1] in res_dct[prep[0]]['customizations']:
            #print "custom0",prep[1]
            custom = prep[1]

        if prep[1] not in res_dct[prep[0]]['modifiers']  and prep[1] not  in res_dct[prep[0]]['customizations']:
            try:
                if int(prep[1]):
                    size = prep[1]
            except ValueError:
                print('4423i1')
                try:
                    if float(prep[1]):
                        size = prep[1]
                except ValuError:
                    print('4423i1i2')
                    print("Wrong value: %s, can map to any field please check\n\nRegards ItDevOps" % prep[1])
                    sys.exit(2)


        if prep[2] in res_dct[prep[0]]['modifiers']:
            #print "mod",prep[2]
            mod = prep[2]
        if prep[2] in res_dct[prep[0]]['customizations']:
            #print "custom",prep[2]
            custom = prep[2]

        if prep[2] not in res_dct[prep[0]]['modifiers']  and  prep[2] not in res_dct[prep[0]]['customizations']:
            try:
                if int(prep[2]):
                    size = prep[2]
            except ValueError:
                print('4423i1i12')
                try:
                    if float(prep[2]):
                        size = prep[2]
                except ValuError:
                    print('4423i1i32')
                    print("Wrong value: %s, can map to any field please check\n\nRegards ItDevOps" % prep[2])
                    sys.exit(2)

        if prep[3] in res_dct[prep[0]]['modifiers']:
            mod = prep[3]
        if prep[3] in res_dct[prep[0]]['customizations']:
            custom = prep[3]

        if prep[3] not in res_dct[prep[0]]['modifiers']  and prep[3] not in res_dct[prep[0]]['customizations']:
            try:
                if int(prep[3]):
                    size = prep[3]
            except ValueError:
                print('4423i1i325')
                try:
                    if float(prep[3]):
                        size = prep[3]
                except ValueError:
                    print('4423i1i326')
                    print("Wrong value: %s, can map to any field please check\n\nRegards ItDevOps" % prep[3])
                    sys.exit(2)

        string.append(json.dumps({'image':prep[0],'size':size,'mod':mod,'custom':custom}))

    return string
