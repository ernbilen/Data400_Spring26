# Tommy Eaton Data 400 Idea 1 Document:

# Research Question:

- Do high school cellphone policies improve student academic performance measured through graduation rates, attendance and engagement between 2023 and 2025?

# 1. Tractable Data:
| Data location | Contents |
| ------ | ------ |
| NCES School Pulse Panel (SPP) | Nationally available cellphone policy data including whether a school has a cell phone policy, types of policy, school characteristics, attendance/behavior indicators, State and District Identifiers.  |
| The EdFacts Data Collection  |Provides nationwide, school level data on attendance, chronic absenteeism, graduation rates, and assessment performance. |

### Why am I using two different datasets? 

- There is not a single database that includes the three inportant varibles that I want to use in my model which is school cell phone policies, graduation rates of students and assessment performace. 
- The School Pulse Panel is the only nationwide dataset that directly measures cellphone policy adoption and enforcement at the school level.
- EdFacts is the only nationwide, standardized dataset that includes school level academic performance indicators for every public school in the U.S.
- Because GPA is unavailable nationwide, I will use graduation rates, attendance, chronic absenteeism, and assessment performance as standardized academic outcome measures.
- I am also going to have to focus on a few specific states because the EdFacts data is by state. So I will pick 2 states with cell phonbe policies and 2 without. 



# 2. Data Retrieval:
- SPP Retrieval: Download the annual SSP files from NCES website from 2023-2025 and only extract the variables	Cellphone policy indicators and School identifiers. [NCES School Pulse Panel](https://nces.ed.gov/surveys/spp/results.asp)
- EDFacts Retrieval: Download the Annual EdFacts files from the EDFACTS website from 2023-2025 and only extract the variables attendance, chronic absenteeism, graduation rates, assessment performance and demographics. [EDFacts](https://www.ed.gov/search?search_api_fulltext=Data&aggregated_field%5Bmin%5D=&aggregated_field%5Bmax%5D=&facet_topic%5B2297%5D=2297&sort_bef_combine=search_api_relevance_DESC&page=1)

# 3. Specification of the Model: 

- I will Be using a Difference in Differences Model that compares schools that have cellphone policies to those who do not and how these policies effect graduation rates, assessment performance and attendence. 
- A baseline or other forms of a DiD model is the simplest and best way to estimate whether cellphone policies cause changes in graduation rates, attendance, and assessment performance by comparing how schools who have or dont have cell phone policies change the acedemic performace of their students over time.

# 4. Implications for Stakeholders: 
- The topic of cellphone bans is relatively new and their is very minimal data on how it effects students academic performace. Study's on this topic are more focused on student engagement, cyberbullying, use of AI/cheating, overall health and well being of students health. 
- The stakeholders for my project are Parents, Teachers, Students and Administrators of schools in the united states either with or without cell phone policies. 
- Parents can use the information from my project to help properly inform them on their decision making it terms of whether or not they support these policies in schools and whether these policies are beneficial to their children while in school. 
- Teachers can use the information from my project to help show them whether or not these cell phone policies are beneficial or detrimental to their students as well as their classroom enviorment. As well as inform them to whether or not they should support these policies in schools. 
- Students can use the information from my project to inform them on the outcomes of these policies because they are at the center of these policies. Specifically whether they are positive or negative impacts and whether or not they need to do something to address this by talking to parents, teachers or administrators. 
- Administrators can use the information from my project to inform them on whether or not the policies that they put into place are effective and the solution to the problem they are trying to address or if they need to try and address the problems another way. 

# 5. Ethical, Legal and Societal implications:
- The main ethical implications of this project is to show if these policies are actually beneficial for the students in these schools academically. Through other studies it has been shown that these policies are beneficial for the other issues including student engagement, cyberbullying, use of AI/cheating, overall health and well being of students health. All of these issues are all trying to address the same ethical dilemma which is it ethical to prevent a student access to their cellphone during the school day, and with so many stakeholders involved it is a very  difficult question to answer. 
- Legal implications would be is it possible to make these cell phone policies a federal mandate, because as of now they are only state or district wide so it is the state or districts decision. Another legal implication would be do these cellphone policies put the school in danger legally if a stuudent is unable to contact their parents in a time of need.
- Societal Implications would be this project could show how effective or ineffective these cell phone policies are academically for students and could impact how schools across the united states address their students and cell phones in their schools. 