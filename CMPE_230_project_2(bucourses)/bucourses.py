#!/usr/bin/env python3
programs = ['MANAGEMENT', 'ASIAN+STUDIES', 'ASIAN+STUDIES+WITH+THESIS', 'ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY', 'AUTOMOTIVE+ENGINEERING', 'MOLECULAR+BIOLOGY+%26+GENETICS', 'BUSINESS+INFORMATION+SYSTEMS', 'BIOMEDICAL+ENGINEERING', 'CRITICAL+AND+CULTURAL+STUDIES', 'CIVIL+ENGINEERING', 'CONSTRUCTION+ENGINEERING+AND+MANAGEMENT', 'COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY', 'EDUCATIONAL+TECHNOLOGY', 'CHEMICAL+ENGINEERING', 'CHEMISTRY', 'COMPUTER+ENGINEERING', 'COGNITIVE+SCIENCE', 'COMPUTATIONAL+SCIENCE+%26+ENGINEERING', 'ECONOMICS', 'EDUCATIONAL+SCIENCES', 'ELECTRICAL+%26+ELECTRONICS+ENGINEERING', 'ECONOMICS+AND+FINANCE', 'ENVIRONMENTAL+SCIENCES', 'ENVIRONMENTAL+TECHNOLOGY', 'EARTHQUAKE+ENGINEERING', 'ENGINEERING+AND+TECHNOLOGY+MANAGEMENT', 'FINANCIAL+ENGINEERING', 'FOREIGN+LANGUAGE+EDUCATION', 'GEODESY', 'GEOPHYSICS', 'GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING', 'HISTORY', 'HUMANITIES+COURSES+COORDINATOR', 'INDUSTRIAL+ENGINEERING', 'INTERNATIONAL+COMPETITION+AND+TRADE', 'CONFERENCE+INTERPRETING', 'INTERNATIONAL+TRADE', 'INTERNATIONAL+TRADE+MANAGEMENT', 'LINGUISTICS', 'WESTERN+LANGUAGES+%26+LITERATURES', 'LEARNING+SCIENCES', 'MATHEMATICS', 'MECHANICAL+ENGINEERING', 'MECHATRONICS+ENGINEERING', 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST', 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS', 'MANAGEMENT+INFORMATION+SYSTEMS', 'FINE+ARTS', 'PHYSICAL+EDUCATION', 'PHILOSOPHY', 'PHYSICS', 'POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS', 'PRIMARY+EDUCATION', 'PSYCHOLOGY', 'MATHEMATICS+AND+SCIENCE+EDUCATION', 'SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION', 'SYSTEMS+%26+CONTROL+ENGINEERING', 'SOCIOLOGY', 'SOCIAL+POLICY+WITH+THESIS', 'SOFTWARE+ENGINEERING', 'SSOFTWARE+ENGINEERING+WITH+THESIS', 'TURKISH+COURSES+COORDINATOR', 'TURKISH+LANGUAGE+%26+LITERATURE', 'TRANSLATION+AND+INTERPRETING+STUDIES', 'SUSTAINABLE+TOURISM+MANAGEMENT', 'TOURISM+ADMINISTRATION', 'TRANSLATION', 'EXECUTIVE+MBA', 'SCHOOL+OF+FOREIGN+LANGUAGES']
departments = ['AD', 'ASIA', 'ASIA', 'ATA', 'AUTO', 'BIO', 'BIS', 'BM', 'CCS', 'CE', 'CEM', 'CET', 'CET', 'CHE', 'CHEM', 'CMPE', 'COGS', 'CSE', 'EC', 'ED', 'EE', 'EF', 'ENV', 'ENVT', 'EQE', 'ETM', 'FE', 'FLED', 'GED', 'GPH', 'GUID', 'HIST', 'HUM', 'IE', 'INCT', 'INT', 'INTT', 'INTT', 'LING', 'LL', 'LS', 'MATH', 'ME', 'MECA', 'MIR', 'MIR', 'MIS', 'PA', 'PE', 'PHIL', 'PHYS', 'POLS', 'PRED', 'PSY', 'SCED', 'SCED', 'SCO', 'SOC', 'SPL', 'SWE', 'SWE', 'TK', 'TKL', 'TR', 'TRM', 'TRM', 'WTR', 'XMBA', 'YADYOK']

import pandas as pd
import re #added for regex
import sys

def singleterm(totalinstrset,term, y, z):
    dname = '(' + z.replace('+',' ') + ')'
	#transform semesters into needed format
    if(term[6] == 'a'):
        x = term[:4]+ "/" + str(int(term[:4])+1) +"-" + '1'
    elif(term[6] == 'p'):
        x = str(int(term[:4])-1) + "/" + term[:4] + "-" + '2'
    elif(term[6] == 'u'):
        x = str(int(term[:4])-1) + "/" + term[:4] + "-" + '3'
	#get the table of the wanted department in the given semester	
    tables = pd.read_html("http://registration.boun.edu.tr/scripts/sch.asp?donem="+x+"&kisaadi="+y+"&bolum="+z,header=0)
    df = tables[3]
    df = df[["Code.Sec","Name","Instr."]]
    df.insert(0,"Dept./Prog. (name)", " ")
	#add a columns filled with x's next to course names
    df.insert(3,term,"x")
    df = df[df["Instr."] != "STAFF STAFF"] #Check before finishing the project
    df = df[df["Name"] != "P.S."]
    df = df[df["Name"] != "LAB"]
	#transform to set to remove duplicates
    instructorset = set(df["Instr."].tolist())
    totalinstrset.update(instructorset)
    dfn = pd.DataFrame({'Dept./Prog. (name)' : y + z  , 'Code.Sec' : 'NaN', 'Name' : 'NaN', term:'NaN', 'Instr.':'NaN' },index = [0])
    df = pd.concat([dfn,df], sort = False).reset_index(drop = True)
    df["Code.Sec"] = df["Code.Sec"].str[:-3]
    justforinst = df[["Code.Sec",'Instr.']]
    df = df[['Dept./Prog. (name)', "Code.Sec","Name", term]]
    
    
    df = df.drop_duplicates()
    df = df.reset_index(drop = True)
    undergrad = 0
    grad = 0
    instructornum = len(instructorset)
    for i in df["Code.Sec"].tolist():
        if(len(i) <= 3 ):
            continue
        if(not i[-3].isdigit() or int(i[-3])<=4 ):#if the course code doesn't involve letters instead of numbers or the number is less then or equal to 4 increment the undergrad
            undergrad = undergrad + 1
        else:#if the course number is bigger then 4 increment grad
            grad = grad + 1

    df.iloc[0,3] = "U" + str(undergrad) + " G" + str(grad) + " I" + str(instructornum)
    return df,justforinst
#from initerm to finterm process the given department(deptname) 
def processdepartment(initerm,finterm,deptshort,deptname):
    totalinstrset = set()
    termlist = []
    cleantermlist = []
    currentterm = initerm
    sp = "Spring"
    su = "Summer"
    fa = "Fall"
	#create termlist
    while(currentterm != finterm):
        termlist.append(currentterm)
        if(currentterm[5:] == sp):
            currentterm = currentterm[:5] + su
        elif(currentterm[5:] == su):
            currentterm = currentterm[:5] + fa
        elif(currentterm[5:] == fa):
            currentterm = str(int(currentterm[:4])+1) + "-" + sp
    termlist.append(finterm)
    #traverse through the termlist and check wherher this dept exists in current term
	#if it exists add that term to the cleantermlist
    for term in termlist:
        if(term[6] == 'a'):
            x = term[:4]+ "/" + str(int(term[:4])+1) +"-" + '1'
        elif(term[6] == 'p'):
            x = str(int(term[:4])-1) + "/" + term[:4] + "-" + '2'
        elif(term[6] == 'u'):
            x = str(int(term[:4])-1) + "/" + term[:4] + "-" + '3'
        try:
            tables = pd.read_html("http://registration.boun.edu.tr/scripts/sch.asp?donem="+x+"&kisaadi="+deptshort+"&bolum="+deptname,header=0)
            cleantermlist.append(term)
        except:
            continue
        
    if(len(cleantermlist) == 0):
        return pd.DataFrame({'Dept./Prog. (name)':'NaN'},index = [0]).drop([0])
    
    
    #call singleterm method with the legal termlist, create first table
    df, insttable = singleterm(totalinstrset,cleantermlist[0],deptshort,deptname)
    termct = pd.DataFrame({'Code.Sec' : 'NaN'},index = [0])#empty dataframe
	#merge other terms with the existing table(df)
    for i in cleantermlist:
        temp1,temp2 = singleterm(totalinstrset,i,deptshort,deptname)
        termct = termct.append(temp1[['Code.Sec']])#derlser uc uca eklendi
        df = df.merge(temp1,how = "outer")
		#table for instructors
        insttable = insttable.merge(temp2,how = "outer")
	#add a count column next to the Code.Sec(termct table)
	#all courses have 1 next to it, so we can use groupby and sum to calculate how many times the course is opened
    termct['termcount'] = 1	
    termct = termct.groupby('Code.Sec').sum()
    termct = termct[1:]	
    #print(termct)
    df = pd.merge(df, termct, how='outer', on=['Code.Sec'])
    df['termcount'] = df['termcount'].map(lambda x: str(x)[:-2])
	#to count the instructors after dropping duplicates,we add a column filled with 1 next to instructors
	#then groupby and sum to calculate how many distinct instructor teaching each course
    insttable = insttable.drop_duplicates()
    insttable = insttable.reset_index(drop = True)
    insttable = insttable.drop(insttable.index[0])
    insttable['incount'] = 1
    insttable = insttable.groupby("Code.Sec").sum()
    df = pd.merge(df, insttable, how='outer', on=['Code.Sec'])
    df['incount'] = df['incount'].map(lambda x: str(x)[:-2])
    df = df[:-1]
	#write Total Offerings column and delete incount and termcount
    df["Total Offerings"] = df["incount"].map(str) + "/" + df["termcount"].map(str)

    df = df.drop(['incount', 'termcount'], axis=1)
    #print(df) #previous stable version
    undergradcount = 0
    gradcount = 0
	#calculate the number of undergraduate and graduate courses in every term
    for term in cleantermlist:
        und = re.search(r'U(\d*)\s',df[term][0]).group()
        gra = re.search(r'G(\d*)\s',df[term][0]).group()
        undergradcount += int(und[1:-1])
        gradcount += int(gra[1:-1])

    df.iloc[0,-1] = 'U' + str(undergradcount) + ' G' + str(gradcount) + ' I' + str(len(totalinstrset))
    
    
    df.iloc[0,2] = ' '
    return df


initerm = sys.argv[1]
finterm = sys.argv[2]
deptlist = programs
deptshort = departments

wholetable = pd.DataFrame({'Dept./Prog. (name)':'NaN'},index = [0])
wholetable = wholetable.drop([0])
#for all departments in the department list call processdepartment and append every department to the original table
for i in range(0,len(deptlist)):
    df = processdepartment(initerm,finterm,deptshort[i],deptlist[i])
    wholetable = wholetable.append(df,sort = False)

wholetable = wholetable.fillna(' ')
wholetable = wholetable.rename(index=str, columns={"Code.Sec": "Course Code", "Name": "Course Name"})
wholetable = wholetable.to_csv(index=False)
print(wholetable)