import streamlit 
streamlit.title("My parents new healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))
#fruits_selected =streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

#fruits_to_show = my_fruit_list.loc[fruits_selected]

#New section for fruit_load_list api

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)

#New section for fruit_load_list
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)


# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

#import snowflake.connector
import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")   #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall() #my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")   #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
streamlit.dataframe(my_data_rows)    #streamlit.text(my_data_row)
#adding a fruit insert into table
add_my_fruit=streamlit.text_input('What fruit would you like add?')

streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")  #my_cur.execute("insert into fruit_load_list")

# to stop streamlit
streamlit.stop()
