#client


from dcm import data_chunking_level_1
from oir import optical_image_recognition
import time
import PythonMagick as pm 
import os
from mine import primary_search
from mine import secondary_search






height=1200
width=1000

skip_color_start=170
skip_color_end=225

blue=0
red=0
green =0

primary_row=[9,254,165]
secondary_col=[8,255,-1]
secondary_row=[5,254,165]



key_word_name = 'name'
key_word_test_start = 'test name'
key_word_test_end = 'please correlate'


index_of_name_chunk = 2
index_of_test_start_idetifier = 3
index_of_test_end_idetifier = index_of_test_start_idetifier+2

identifier_row = 1
identifier_column = 1



input_pdf_name = raw_input("enter file name: ")
os.system("pdftk "+input_pdf_name+" Burst output pages/pdf_name%02d.pdf")

img = pm.Image()
img.density("500")

for page in os.listdir("pages"):
    if page.endswith(".pdf"):
        img.read("pages/"+page)
        img.write("image/"+str(page.split('.')[0])+".jpg")
                
        
name_start = []
test_start = []
test_end  = []
name_data = []
test_data = []
    

for item in os.listdir("image"):
    if item.endswith(".jpg") or item.endswith(".png"):
        image = "image/"+item
        chunking = data_chunking_level_1(height,width,skip_color_start,skip_color_end)
        oir=optical_image_recognition()
        out_final=[]
        horizontal_chunks = []

        start_t = time.time()
        data_dict,gray,horizontal_chunk_index= chunking.draw_table_on_image_file(image,primary_row,secondary_col,secondary_row)
        horizontal_chunks.append(horizontal_chunk_index)

        out=oir.crop_image(gray,data_dict)
        find_start = primary_search()
        data_list  = find_start.clean_data(out.tolist()) 
        name_start_index = find_start.data_division_start(data_list,key_word_name, index_of_name_chunk, identifier_row, identifier_column)
        name_start.append(name_start_index)
        test_start_index = find_start.data_division_start(data_list,key_word_test_start, index_of_test_start_idetifier, identifier_row, identifier_column)
        test_start.append(test_start_index)
        test_end_index  = find_start.data_division_end(data_list,key_word_test_end,test_start_index)
        test_end.append(test_end_index)
        secondary_division = secondary_search()
        divided_data_name = secondary_division.secondary_division(name_start_index,test_start_index,data_list)
        name_data.append(divided_data_name)
        test_divided_data = secondary_division.secondary_division(test_start_index,test_end_index,data_list)
        test_data.append(test_divided_data)
       
print(name_data)

print('\n')
print('\n')
print('\n')

print(test_data)

