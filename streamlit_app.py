import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom new healthy dinner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 kale,Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocardo toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page
streamlit.dataframe(my_fruit_list)

streamlit.multiselect("Pick some fruits :" ,list(my_fruit_list.index),['Apple' , 'Banana'])

fruits_selected = streamlit.multiselect("Pick some fruits" , list(my_fruit_list.index),['Apple' , 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
   fruityvice_repsonse = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   fruitvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
  

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    #streamlit.write('The user entered ', fruit_choice)
    streamlit.error(" Please select a fruit to get information. ")
  else:
    back_from_function =  get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
      # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/Apple " +"kiwi")
#       fruityvice_repsonse = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#       fruitvice_normalized = pandas.json_normalize(fruityvice_response.json())
#       streamlit.dataframe(fruityvice_normalized)
      
except URLError as e :  
    streamlit.error()

streamlit.stop()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header(" The Fruit load list contains:")
# streamlit.dataframe(my_data_rows)

streamlit.header(" The Fruit load list contains:")
# Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
# add a button to load fruit
if streamlit.button ('Get Fruit Load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)


fruit_choice = streamlit.text_input('what fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', fruit_choice)

my_cur.execute("insert into fruit_load_list values(' from streamlit')")
