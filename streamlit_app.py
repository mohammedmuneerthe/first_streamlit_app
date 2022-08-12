import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import streamlit 
streamlit.title("My parents new healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))
#fruits_selected =streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

#fruits_to_show = my_fruit_list.loc[fruits_selected]

#New section for fruit_load_list api

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
#create a function
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return (fruityvice_normalized)
	

#New section for fruit_load_list
streamlit.header("Fruityvice Fruit Advice!")
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please select a fruit to get infromation.")
	else:
		back_from_function=get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)
except URLError as e:
	streamlit.error()
#####################
# try: 
#  fruit_choice = streamlit.text_input('What fruit would you like information about?')
#     if not fruit_choice:
#         streamlit.error("Please select a fruit to get infromation.")
#     else:
# 	 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#       	 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()
# 	 streamlit.dataframe(fruityvice_normalized)

# except URLError as e:
# 	streamlit.error()
##############################
#import snowflake.connector
# to stop streamlit
################################
#streamlit.stop()
#import snowflake.connector
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")   #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_rows = my_cur.fetchall() #my_data_row = my_cur.fetchone()
#streamlit.header("The fruit load list contains:")   #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#streamlit.dataframe(my_data_rows)    #streamlit.text(my_data_row)
#######################################
streamlit.header("Fruityvice Fruit Advice!")
#snowflake realted function
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from fruit_load_list")
		return my_cur.fetchall()
#add a button to load the fruit
if streamlit.button('Get Fruit Load list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows=get_fruit_load_list()
	streamlit.dataframe(my_data_rows)

##########################
#adding a fruit insert into table
#add_my_fruit=streamlit.text_input('What fruit would you like add?')

#streamlit.write('Thanks for adding', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")  #my_cur.execute("insert into fruit_load_list")
#####################
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into fruit_load_list values ('from streamlit')")
		return "Thanks for adding" + new_fruit
add_my_fruit=streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a  Fruit to Load list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function=insert_row_snowflake(add_my_fruit)
	streamlit.dataframe(back_from_function)

