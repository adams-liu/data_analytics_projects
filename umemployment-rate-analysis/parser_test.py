# text_parser.py this script just extracts the most used skill words

import re 


def getSkillsList():
    technical_skills = open("technical_skills.txt","r") 
    technical_skills_ls = technical_skills.readlines()
    return [skill[:-1] for skill in technical_skills_ls]

# technical_skills_ls = getSkillsList()

def printKeywords(description,technical_skills_ls):
    # file1 = open("description.txt","r") 
    # description1 = file1.readlines()
    description = description.splitlines()
    # print(type(description))
    # print(type(description1))

    word_list = ['experience', 'year', 'skill','knowledge','technologies','degree','develop', 'software', 'programming','familiar','proficien','understand','ability']
    temp_list = []
    year_sentences = []

    for sentence in description:
        if any(word in sentence for word in word_list):
            temp_list.append(sentence)
            
            if 'year' in sentence:
                year_sentences.append(sentence)
                
    years = []
    for sentence in year_sentences:
        for s in re.findall(r'-?\d+\.?\d*', sentence):
            years.append(int(s))


    temp_set = set()

    for skill in technical_skills_ls:
        for sentence in temp_list:
            if skill in sentence:
                if (skill == "c/c++" ):
                    temp_set.add('c/c++')
                elif (skill == 'c++'):
                    temp_set.add('c++')
                else:
                    try:
                        if(re.findall(skill+'\\b', sentence)):
                            temp_set.add(skill)
                    except:
                        print("Error on skill: " + skill)


    min_years = 0  
    if years:
        min_years = min(years)

        

    return min_years,list(temp_set)           

