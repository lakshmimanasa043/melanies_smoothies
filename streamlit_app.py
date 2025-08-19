#import Python Packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Input: Name on order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get fruit options from Snowflake
cnx=st.connection("snowflake")
session = cnx.session()
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_df.collect()]

# Let user pick fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Only proceed if ingredients are selected
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        

    # Prepare insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}');
    """

    # Optional: show the insert query for debugging
    # st.write(my_insert_stmt)

    # Submit button inside valid condition
    if st.button('Submit Order'):
        try:
            session.sql(my_insert_stmt).collect()
            st.success('✅ Your Smoothie is ordered,Betty jean! ')
        except Exception as e:
            st.error(f'❌ Error placing order: {e}')
else:
    st.info("👉 Please enter a name and select at least one ingredient.")
   
   
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
