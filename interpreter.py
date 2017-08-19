import sys
import time
import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)
import time

class image_interpreter():

    def __init__(self,red,green,blue):
        self.red = red
        self.blue = blue
        self.green = green
              
    def draw_on_image(self,image,cordinates_list=[[]]):
        start_t = time.time()
        image = cv2.line(image,(cordinates_list[0][0],cordinates_list[0][1]),(cordinates_list[1][0],cordinates_list[1][1]),(self.blue,self.green,self.red),1)    
        end_t = time.time()
#         print("draw_on_image: "+str(end_t-start_t))
        return image
    
    def display_image(self,image_name,window_name):
        start_t = time.time()
        cv2.imshow("view",image_name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        end_t = time.time()
#         print("display_image: "+str(end_t-start_t))
    def draw_primary_row_chunks(self,image,height,width,horizontal_chunk_index):
        start_t = time.time()
        img = cv2.imread(image)
        resized_image = cv2.resize(img, (width,height)) 
        for index in horizontal_chunk_index:
            image=self.draw_on_image(resized_image,[[0,index],[width,index]])
        self.display_image(image,"view")
        end_t = time.time()
#         print("draw_primary_row_chunks: "+str(end_t-start_t))   
    def draw_table(self,image,data_dict):
        start_t = time.time()
        img = cv2.imread(image)
        resized_image = cv2.resize(img, (data_dict["width"],data_dict["height"]))
        for inner_dict in data_dict["chunk"]:
            start = inner_dict['start']
            end = inner_dict['end']
            column_list = inner_dict['columns']
            row_list = inner_dict['rows']                                                   
            image=self.draw_on_image(resized_image,[[0,start],[data_dict["width"],start]])
                                                               
            for column in column_list:
                image=self.draw_on_image(image,[[column,start],[column,end]])
             
            for row in row_list:
                 image=self.draw_on_image(image,[[0,row],[data_dict["width"],row]])                                              
        
        self.display_image(image,"view")    
        end_t = time.time() 
#         print("draw_table: "+str(end_t-start_t))
    def print_output_data(self,data):
        start_t = time.time()
        for primary_row in data:
            for secondary_row in primary_row:
                for secondary_column in secondary_row:
                    if type(secondary_column) is dict:
                        if secondary_column['text'] is '':
                            sys.stdout.write('\t')
                        else:
                            sys.stdout.write(secondary_column['text'].replace("\n"," ")+"\t")
                sys.stdout.write("\n")
            sys.stdout.write("\n\n")
        end_t = time.time()
#         print("print_output_data: "+str(end_t-start_t))
    
    
