#!/usr/bin/env python
# coding: utf-8

# In[48]:


# pip install openai==0.28


# ### Here, I imported all the libraries

# In[20]:


import base64
import json
import os
import openai
from PIL import Image
from IPython.display import display, Markdown
import matplotlib.pyplot as plt


# ### This function is used to extract PlantUML code from the output

# In[21]:


def extract_and_display_code(message):
    start_index = message.find("@startuml")
    end_index = message.find("@enduml")
    if start_index != -1 and end_index != -1:
        extracted_code = message[start_index:end_index + len("@enduml")]
        return display(Markdown("```plantuml\n{}\n```".format(extracted_code)))
    else:
        return "1"


# ### This function encodes the image into base64 format.

# In[22]:


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
api_key = "your api-key"
openai.api_key = api_key


# ## Approach: ( First Approach )
# ### First i generated the description of the UML image and then I used the UML image and the image description to generate PlantUML code using GPT - 4 vision preview. This approach wasn't showing good results.

# In[23]:


def generate_description_from_image(image_url):
    response = openai.ChatCompletion.create(
        model='gpt-4-vision-preview', 
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text":  "Describe a PlantUML diagram depicting a user authentication flow and such that it's description can be used to generate PlantUML code .CORRECTLY check whether it is a participant or actor and also the colour.FOCUS ON EVERY MINUTE DETAIL."},
                    {
                        "type": "image_url",
                        "image_url": image_url
                    }
                ],
            }
        ],
        max_tokens=300,
    )
    description = response.choices[0].message.content

    return description


# In[24]:


def generate_plantuml_code(description, image_url):
    response = openai.ChatCompletion.create(
        model='gpt-4-vision-preview',
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": description}, 
                    {
                        "type": "image_url",
                        "image_url": image_url
                    },
                    {"type": "text", "text": "Generate the PlantUML code using the above description and the image, now correct the PlantUMLcode for every minute difference between the image and code depicting the image."}
                ],
            }
        ],
        max_tokens=250,
    )
    plantuml_code_response = response.choices[0].message.content
    return plantuml_code_response


# ### Below is the test sample

# In[41]:


image_local = "D:\\HP\\users\\OneDrive\\Pictures\\Screenshots\\Screenshot 2024-04-09 160445.png"
image = Image.open(image_local)
plt.imshow(image)
plt.axis('off')
plt.show()


# In[25]:


image_url = f"data:image/png;base64,{encode_image(image_local)}"
description = generate_description_from_image(image_url)
plantuml_code = generate_plantuml_code(description, image_url)
print("Generated PlantUML code:")

if (extract_and_display_code(plantuml_code))!= "1" :
    f = 0
    pass
else:
    if (extract_and_display_code(description))!= "1" :
        pass
    else:
        print(plantuml_code)


# 
# ## OUTPUT using 1st approach
# # 

# ![image.png](attachment:image.png)

# ## Second Approach :
# ### Directly generate PlantUML code and description from the image by providing image and prompt to GPT - 4 vision Preview and then extracting a PlantUML code from the response.

# In[27]:


print("Generated PlantUML code:")
if (extract_and_display_code(description))!= "1" :
    pass
else:
    print(plantuml_code)


# 
# ## OUTPUT using 2nd approach
# # 

# ![image-2.png](attachment:image-2.png)

# ## Third Approach:
# 
# ### To save the credits the, we  can minimize the cost by using 
# - "gpt-4-vision-preview" will be used for generating image description.
# - "gpt-3.5-turbo-instruct" for generating PlantUML code using above description.
# - It will reduce the token cost 1 by 10th to 1 by 100th.

# In[45]:


# To implement this approach just change the function:          def generate_plantuml_code(description, image_url):
def generate_plantuml_code(description):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": description}, 
                    {"type": "text", "text": "Generate the PlantUML code using the above description and the image, now correct the PlantUMLcode for every minute difference between the code depicting the image and the description."}
                ],
            }
        ],
        max_tokens=250,
    )
    plantuml_code_response = response.choices[0].message.content
    return plantuml_code_response


# In[46]:


description = generate_description_from_image(image_url)
plantuml_code = generate_plantuml_code(description)
print("Generated PlantUML code:")

if (extract_and_display_code(plantuml_code))!= "1" :
    f = 0
    pass
else:
    if (extract_and_display_code(description))!= "1" :
        pass
    else:
        print(plantuml_code)


# ### To compare the results you can copy above code and paste it here [ https://www.planttext.com/ ] and compare with the original UML image.

# 
# ## OUTPUT using 3rd approach
# # 

# ![image-2.png](attachment:image-2.png)

# In[ ]:




