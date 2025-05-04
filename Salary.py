import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
salary_data = pd.read_csv("Salary_Data.csv")
print(salary_data.info())
salary_data.dropna(inplace=True)
print(salary_data["Education Level"].value_counts())
def UnifyEducationLevel(s):
    for e in ['Bachelor','Degree','Master','PhD','High','School']:
        if e.lower() in s.lower(): return e
    return s
salary_data['Education Level'] = salary_data['Education Level'].apply(UnifyEducationLevel)
print(salary_data["Education Level"].value_counts())
print("="*40)
salary_data["Age"] = salary_data["Age"].astype('int')
salary_data["Years of Experience"] = salary_data["Years of Experience"].astype('int')
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12,8))
fig.suptitle('Статистика опросов', fontsize=16)
salary_data['Age'].plot(kind='hist', ax=axes[0,0], title='Возраст')
salary_data['Gender'].value_counts().plot(kind='bar', ax=axes[1,0], title='Пол')
salary_data['Education Level'].value_counts().plot(kind='bar', ax=axes[0,1], title='Образование')
salary_data['Job Title'].value_counts()[:10].plot(kind='bar', ax=axes[1,2], title='Должность')
salary_data['Years of Experience'].plot(kind='hist', ax=axes[0,2], title='Стаж работы')
salary_data['Salary'].plot(kind='hist', ax=axes[1,1], title='Зарплата')
plt.tight_layout()
plt.show()
