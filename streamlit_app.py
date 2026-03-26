# Import python packages.
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app.
st.title(f"Customize your smoothies :cup_with_straw: ")

name_on_order=st.text_input('Name on Smoothie :')
st.write('Your name on the smoothie will be:',name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select (col(
    "fruit_name"
))
ingredient_list=st.multiselect(
    'Choose upto 5 ingredients : ',
    my_dataframe,
    max_selections=5
)


if ingredient_list:
    

    ingredient_string=''

    for each_fruit in ingredient_list:
        ingredient_string+=each_fruit + ' '
        st.subheader(each_fruit+ 'Nutrition_Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ each_fruit)  
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    st.write(ingredient_string)    


    my_insert_stmnt="""insert into smoothies.public.orders
                         (ingredients,name_on_order) values('"""+ingredient_string+"""'
                         ,'"""+name_on_order+"""') """

    time_to_insert=st.button("Submit Order")

    
    if time_to_insert:
        session.sql(my_insert_stmnt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")




