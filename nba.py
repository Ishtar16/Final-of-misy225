import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')

st.title('NBA salary analysis (2020)')

df = pd.read_csv('nbasalarystats.csv')


# add score sliders
score_slider = st.slider('Minimal PTS', 0, 35, 10)
df = df[df.PTS >= score_slider]

score_slider2 = st.slider('Maximum PTS', 0, 35, 15)
df = df[df.PTS <= score_slider2]

AST_slider = st.slider('Minimal AST', 0, 13, 3)
df = df[df.AST >= AST_slider]

AST_slider2 = st.slider('Maximum AST', 0, 13, 5)
df = df[df.AST <= AST_slider2]

TRB_slider = st.slider('Minimal TRB', 0, 17, 5)
df = df[df.TRB >= TRB_slider]

TRB_slider2 = st.slider('Maximum TRB', 0, 17, 10)
df = df[df.TRB <= TRB_slider2]


# add a position multi selector
pos_filter = st.sidebar.multiselect(
     'Choose players\' position',
     df.Pos.unique(),  # options
     df.Pos.unique())  # defaults

df = df[df.Pos.isin(pos_filter)]

# add a radio button widget
player_age = ['Low (24-)', 'Median (25-32)', 'High (32+)', 'All']
age_filter = st.sidebar.radio('Choose age level', player_age)
if age_filter == 'Low (24-)':
    df = df[df.Age <= 24]
elif age_filter == 'All':
    df = df
elif age_filter == 'Median (25-32)':
    df = df[(24 < df.Age) & (df.Age< 32)]
else:
    df = df[df.Age >= 32]


# input box
form = st.sidebar.form("Team")
team_filter = form.text_input('Team Name (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")

if team_filter!='ALL':
    df = df[df.Tm == team_filter]


# show df
st.write(df)

# histgram
st.header('Salary levels related to performance')
st.write(f'The median number is $ {df.Salary.median()}')
st.write(f'The max salary is $ {df.Salary.max()}')
st.write(f'The minimum salary is $ {df.Salary.min()}')
st.write(f'The total salary is $ {df.Salary.sum()}')
fig, ax = plt.subplots()
sal_data = df.Salary
sal_data.plot.hist(ax=ax, bins=30)
ax.set_xlabel('Salary')
st.pyplot(fig)

# bar plot
st.header('Salary of different positions')
fig, ax = plt.subplots()
pos_sum = df.groupby('Pos')['Salary'].sum()
pos_sum.plot.bar(ax=ax)
st.pyplot(fig)

# scatter plot
st.header('Relationship between Salary and Player Efficiency (calculated by our group)')
fig, ax = plt.subplots(figsize=(5,5))
df.plot.scatter(ax=ax, x='PER', y='Salary')
st.pyplot(fig)
