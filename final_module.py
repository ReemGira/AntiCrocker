import semantic.semantic_module1 as sm1
import semantic.predict as sm2
import pandas as pd
import xlsxwriter 
#import os
def grade():
    workbook = xlsxwriter.Workbook('C:\\Users\\Reem Salma Amr\\Desktop\\GP all\\website\\flask\\grades.xlsx') 
    worksheet = workbook.add_worksheet()
    data_format1 = workbook.add_format({'bg_color': '#FFC7CE'})
                                        
    worksheet.set_row(0, cell_format=data_format1)
    worksheet.write('A1', 'Student ID') 
    worksheet.write('B1', 'Student Name') 
    worksheet.write('C1', 'Reading') 
    worksheet.write('D1', 'Story') 
    worksheet.write('E1', 'MCQ') 
    worksheet.write('F1', 'Total')
    f = open("semantic/mcq.txt" , "r")
    lines = f.readlines()
    ids = []
    mcq_grades = []
    for i in range ( 0 , len(lines)):
        l = lines[i].split(" ")
        ids.append(int(l[0]))
        l[1]= l[1].replace("\n" , "")
        mcq_grades.append(float(l[1]))
    
    #print(ids)
    #print("\n")
    #print(mcq_grades)  
      
    reading_scores = sm1.grading_module1()
    machine_scores = sm2.semantic_module2()
    
    print(machine_scores)
    #root_dir=os.path.abspath(os.path.dirname(__file__))
    train_df = pd.read_csv("C:\\Users\\Reem Salma Amr\\Desktop\\GP all\\website\\flask\\answers.csv" ,  encoding='latin-1')
    train_df = train_df.iloc[0:]
    type_list = list(train_df['type'])
    degree_list = list(train_df['degree'])
    students_ids = list(train_df['studentID'])
    students_names = list(train_df['Name'])
    i=0 
    x=0
    y=0
    row =2
    while i < len(students_ids):
        xnew = xold = students_ids[i]
        s=0
        r=0
        while xnew == xold:
            
            if i == len(students_ids):
                break
            if(type_list[i] == "reading"):
                #print(i)
                #print(x)
                r+= (degree_list[i] * reading_scores[x])
                x+=1
            elif (type_list[i] == "story"):
                s += (degree_list[i] * machine_scores[y])
                y+=1
                
            i+=1
            if i < len(students_ids)-1:
                xnew = students_ids[i]
        
        s_id = students_ids[i-1]
        s_n = students_names[i-1]
    
        col = 0
        worksheet.write(row, col, s_id)
        worksheet.write(row, col+1, s_n)
        worksheet.write(row, col+2, r)
        worksheet.write(row, col+3, s)
        index = ids.index(s_id)
        
        if index != -1:
            worksheet.write(row, col+4, mcq_grades[index])
            worksheet.write(row, col+5, s + r +mcq_grades[index])
        else:
            worksheet.write(row, col+5, s + r) 
            
        row+=1
        
    workbook.close()            