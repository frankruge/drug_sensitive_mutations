import csv
mutations_file=open("TableS2C_no_headers.csv", "r")
sensitivities_file=open("Table_S4A_no_headers.csv", "r")
dir="/project/folder/"
mutations=mutations_file.readlines()
mutations2=sorted(mutations,key=lambda x: x[1]) #example sort list by column this variable is not used
count=0
tmp=list()
def get_mutations(m_list, cell_line):
    tmp=list()
    for line in m_list:
        # convert line to split list
        l = line.rsplit('\t')
        if l[1] == cell_line:
            tmp.append(l[4])
    return(tmp)

##################################################################################################################
##############################   function call   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv    ############################
#a=get_mutations(mutations, '22RV1')
#print(len(a))
sensitivities=sensitivities_file.readlines()

#sensitivities2=
sensei=sensitivities[0].rsplit('\t')
#print(sensei)
cols_to_grep=[ i for i, word in enumerate(sensei) if word.__contains__('Afatinib') ]
#print(cols_to_grep)
print("getting data for "+ sensei[cols_to_grep[0]])
#for line in sensitivities:

def get_sensitivities(s_list, drug, m_list):
    tmp2=list()
    count=0
    for line in s_list:
        # convert line to split list
        l = line.rsplit('\t')

        tmp2.append([l[1], l[drug], ';'.join(get_mutations(m_list, l[1]))])
        count+=1
        if count==10:
            break
        #print(l)
    #make a nice header
    if tmp2[0][0] == '':
        tmp2[0][0] = 'cell line'
        tmp2[0][2] = 'mutation'
    return(tmp2)

##################################################################################################################
##############################   function call   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv    ############################
aa=get_sensitivities(sensitivities, cols_to_grep[0], mutations)   #Cols_to_grep e.g Afatinib (rescreen), etc.
################################^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#######################################
##################################################################################################################

#now we have a data structure consisting of three columns: "cell line", "Drug sensitivity values" and "Mutations"
#find the middle

#in order to avoid the time-consuming calculations I will just reload the file and comment out the function call
da_file=open("/proj/MLL-AF9_Frank/EMILIO/cell_lines_and_sensitivities_and_mutations_komma.csv", "r")
mutations=mutations_file.readlines()
superlist=list()
for line in da_file:
    l=line.rsplit(',')
    if l[1]=='NA':       #get rid of lines with NA values
        continue #skip the rest of the loop. start a new loop with the next line
    superlist.append([l[0], l[1], l[2]])

low_IC50=list()
high_IC50=list()
divide=3.3
for line in superlist:
    try:
        convert = float(line[1])
    except:
        print("cannot convert to float: "+line[1])
        continue
    if float(line[1]) > divide:
        high_IC50.append(line)
    if float(line[1])<= divide:
        low_IC50.append(line)

#now I have two lists. next I want to list all mutations independent from the cell lines or mutations into other lists
print("low:  "+str(len(low_IC50)))
print("high: "+str(len(high_IC50)))
low=list()
high=list()


def count_mutations(inlist):
    outlist=list()
    for entry in inlist:
        mc = entry[2].rsplit(';')    # mutations celline (mc)
        for gene in mc:
            outlist.append(gene.rstrip())
    outlist=sorted(outlist)
    tmp={}
    for word in outlist:
        tmp[word] = tmp.get(word, 0)+1
    ## after counting, make tuples od gene - count combinations
    tmp2 = []
    for key, value in tmp.items():
        tmp2.append((value,key))
    return(tmp)

l=count_mutations(low_IC50)
print(l)
h=count_mutations(high_IC50)
#so now I have the genes and the counts in two separate tuple lists.
#Problem: if there are genes present in one list and absent in the other.
#1. get full list
#go through genes of merged list. for each gene, write occurrences in low list (0 if absent) and high list(0 if absent). that should do the trick
mut_L=list()
def get_genes(inlist):
    ol=list()
    for entry in inlist:
        mc = entry[2].rsplit(';')    # mutations celline (mc)
        for gene in mc:
            ol.append(gene.rstrip())
    ol=sorted(ol)
    ol2=[]
    for i in ol:
        if i not in ol2:
            ol2.append(i)
    return(ol2)

ll=get_genes(low_IC50)
hh=get_genes(high_IC50)
#merge both lists high low (hl)
hl=[]
for i in ll:
    if i not in hl:
        hl.append(i)
for i in hh:
    if i not in hl:
        hl.append(i)
print(len(ll))
print(len(hh))
print(len(hl))
#now make tuples
finlist=list()
for gene in hl:
    lo=0
    hi=0
    if gene in l:
        lo=l[gene]
    if gene in h:
        hi=h[gene]


    finlist. append([gene,lo,hi, lo-hi])

with open(dir+"TEST.csv",'w') as resultFile:
    wr = csv.writer(resultFile, delimiter= '\t')#dialect='excel')
    for row in finlist:
        wr.writerow(row)


print(ll)
print(hh)

