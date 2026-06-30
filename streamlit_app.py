# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
#import os
import requests  

# Write directly to the app
st.title(f"Customoize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie !
  """
)

title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)


# option = st.selectbox('What is your favourite fruit?', ('Banana','Strawberries','Peaches'))
# st.write('Your favorite fruit is:',option) 

name_on_order = st.text_input('Name on smoothie: ')
st.write('The name on your smoothie will be: ',name_on_order)

# session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

st.dataframe(data=my_dataframe, use_container_width=True)

st.stop()

ingredients_list = st.multiselect('Choose upto 5 ingredientss:', my_dataframe, max_selections=5)

if ingredients_list:
   # st.write(ingredients_list)   # to view as flattened into rows
   # st.text(ingredients_list)    # to view in array list form

   ingredients_string = ''

   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       st.subheader(fruit_chosen + ' Nutrition Information')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
       sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

   st.write(ingredients_string)
   
   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
           values ('""" + ingredients_string + """','""" + name_on_order + """')"""

   #st.write(my_insert_stmt)
   #st.stop
   
   time_to_insert = st.button('Submit Order')

   if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!,' + name_on_order +'!', icon="✅")

