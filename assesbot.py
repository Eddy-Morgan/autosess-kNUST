import requests
from bs4 import BeautifulSoup
import urllib
from numpy.random import choice
import copy

#host KNUST     129.122.16.90:443

class Assess:
    def __init__(self,username,password,studentid):
        self.username = username
        self.password = password
        self.studentid = studentid

    def auto_assesment(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

        login_data = {
            'UserName': '{}'.format(self.username),
            'Password': '{}'.format(self.password),
            'studentid': '{}'.format(self.studentid)
        }

        info = []
        info.append(login_data)
        with requests.Session() as s:
            url = "https://apps.knust.edu.gh/students/"
            login_url = "https://apps.knust.edu.gh/students/Account/Login"
            r = s.get(url, headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name':'__RequestVerificationToken'})['value']
            
            r = s.post(login_url, data = login_data, headers = headers )
            soup = BeautifulSoup(r.content, 'html.parser')
            if soup.find_all("div", {"class": "validation-summary-errors text-danger"}):
                return "Error"
            url = 'https://apps.knust.edu.gh/students/LecturerAssessment'
            r = s.get(url, headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            for iconbar in soup.find_all("span", {'class':'icon-bar'}): 
                iconbar.decompose()
            for lecturer_name in soup.find_all("span", {'style':'font-weight:bolder; color:darkgreen'}):
                lecturer_name.decompose()
            courses = []
            for span in soup.find_all('span'):
                c = urllib.parse.quote(span.string)
                courses.append(c)
            
            for course in courses:
                url = 'https://apps.knust.edu.gh/students/LecturerAssessment/AssessmentForm?CourseCode={}'.format(course)
                r = s.get(url, headers = headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                save_assessment_data = {}

                save_assessment_data['Sem'] = soup.find('input', attrs={'name':'Sem'})['value']
                save_assessment_data['Year'] = soup.find('input', attrs={'name':'Year'})['value']
                save_assessment_data['StaffID'] = soup.find('input', attrs={'name':'StaffID'})['value']
                save_assessment_data['CourseCode'] = soup.find('input', attrs={'name':'CourseCode'})['value']

                credentials = copy.deepcopy(save_assessment_data)
                for name in soup.find_all('strong'):
                    u = name.string
                    course_name, lecturer = u.split('-')
                    credentials['lecturer'] = lecturer
                    credentials['course_name'] = course_name


                info.append(credentials)
        
            
                for n in range(35):
                    if n in [12,13,14,15,16,17,18,19,20]:
                        grade = choice([1])
                    else:
                        grade = choice([1,2,3,4,5], p=[0.1,0.2,0.4,0.2,0.1])

                    save_assessment_data['ChoiceQuestions[{}].Number'.format(n)] = '{}'.format(n+1)
                    save_assessment_data['ChoiceQuestions[{}].Answer'.format(n)] = '{}'.format(grade)

                save_assessment_data['CommentQuestions[0].Number'] = '36'
                save_assessment_data['CommentQuestions[0].Answer'] = '' 

                save_url = 'https://apps.knust.edu.gh/students/LecturerAssessment/SaveAssessment'

                r = s.post(save_url, data = save_assessment_data, headers = headers )
        with open('your_file.txt', 'a+') as f:
            f.write("%s\n" % info)

        return info