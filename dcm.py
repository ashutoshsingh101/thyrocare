
#imports
import cv2
import numpy as np
import time


#level3


class data_chunking_level_3():


    def __init__(self,height,width):
        self.height=height
        self.width=width
    
    def calculate_vector(self,gray,inner,start,end):
        start_t = time.time()
        vector = []
        if inner is False:
            vector = gray.mean(axis=1)
        else:
            primary_gray = np.array(gray.tolist())
            primary_gray = primary_gray[start:end,:]
            primary_gray[primary_gray>=120] = 255
            vector= primary_gray.mean(axis=0)
        end_t = time.time()
#         print("calculate_vector: "+str(end_t-start_t)) 
        return vector

    def primary_segmentation(self,gray,row_vector,primary):
        start_t = time.time()
        
        self.primary_horizontal_skip_pixel=primary[0]
        self.primary_horizontal_threshold=primary[1]
        self.primary_horizontal_line_threshold=primary[2]
        horizontal_chunks_index = [0]
        
        line_detect_temp =  np.array(gray.tolist())
        line_detect_temp[line_detect_temp<=self.primary_horizontal_line_threshold] = 1
        line_detect_temp[line_detect_temp>self.primary_horizontal_line_threshold] = 0
        row_mean = line_detect_temp[:,int(self.width/3):int(2*self.width/3)].mean(axis= 1)
        horizontal_chunks_index.extend(np.where(row_mean==1)[0])
        
        white_space_temp= np.array(row_vector.tolist())
        line_index=np.where(white_space_temp>=self.primary_horizontal_threshold)[0]
        for index in range(len(line_index)):
            temp_value=line_index[index:index+self.primary_horizontal_skip_pixel]-line_index[index]
            if temp_value[len(temp_value)-1]==self.primary_horizontal_skip_pixel:
                 horizontal_chunks_index.append(line_index[index])
        horizontal_chunks_index=np.sort(np.array(horizontal_chunks_index)).tolist()
        
        end_t = time.time() 
#         print("primary_segmentation: "+str(end_t-start_t))
        return horizontal_chunks_index
    
    def accumulate_whitespaces(self,horizontal_chunks_index):
        start_t = time.time()
        deviation_index=0
        while deviation_index <= len(horizontal_chunks_index)-2:
            if horizontal_chunks_index[deviation_index] - horizontal_chunks_index[deviation_index+1] == -1:
                del horizontal_chunks_index[deviation_index]
            else:
                deviation_index= deviation_index+1
                continue
        end_t = time.time()
#         print("accumulate_whitespaces: "+str(end_t-start_t))
        return horizontal_chunks_index


    
    def print_secondary_columns(self,column_vector,secondary_vertical,inner_dict):
        start_t = time.time()
        self.secondary_vertical_skip_pixel=secondary_vertical[0]
        self.secondary_vertical_threshold=secondary_vertical[1]
        self.secondary_vertical_line_threshold=secondary_vertical[2]
        
        line_detect_temp =  np.array(column_vector.tolist())
        line_detect_temp[line_detect_temp<=self.primary_horizontal_line_threshold] = 1
        line_detect_temp[line_detect_temp>self.primary_horizontal_line_threshold] = 0
        mean = line_detect_temp.mean()
        inner_dict["columns"].extend(np.where(mean==1)[0].tolist())
        
        column_flag=False
        whitespace_start_value=0
        for column in range(self.width):
            if column <= self.width-self.secondary_vertical_skip_pixel:
                value=np.mean(column_vector[column:column+self.secondary_vertical_skip_pixel])
                if value >=self.secondary_vertical_threshold:
                    if not column_flag:
                        column_flag=True
                        whitespace_start_value=column
                else:
                    if column_flag:
                        inner_dict["columns"].append(int((whitespace_start_value+column)/2))
                        column_flag=False
        return inner_dict
    
    def print_secondary_rows(self,start_index,end_index,row_vector,secondary_horizontal,inner_dict):
        start_t = time.time()
        self.secondary_horizontal_skip_pixel=secondary_horizontal[0]
        self.secondary_horizontal_threshold=secondary_horizontal[1]
        self.secondary_horizontal_line_threshold=secondary_horizontal[2]

        line_detect_temp =  np.array(row_vector.tolist())
        line_detect_temp[line_detect_temp<=self.secondary_horizontal_line_threshold] = 1
        line_detect_temp[line_detect_temp>self.secondary_horizontal_line_threshold] = 0
        mean = line_detect_temp.mean()
        inner_dict["rows"].extend(np.where(mean==1)[0].tolist())
                
        row_flag=False  
        for row in range(start_index,end_index):
            if row<= end_index -self.secondary_horizontal_skip_pixel:
                value=np.mean(row_vector[row:row+self.secondary_horizontal_skip_pixel])
                if value >= self.secondary_horizontal_threshold:
                    if not row_flag:
                        row_flag=True
                        whitespace_start_value=row
                else:
                    if row_flag:
                        inner_dict["rows"].append(int((whitespace_start_value+row)/2))
                    row_flag=False
        end_t = time.time() 
#         print("print_secondary_rows: "+str(end_t-start_t))
        return inner_dict
    

#level 2


class data_chunking_level_2():
    
    def __init__(self,height,width,skip_color_start,skip_color_end):
        self.height=height
        self.width=width
        self.skip_color_start=skip_color_start
        self.skip_color_end=skip_color_end
        self.d3=data_chunking_level_3(height,width)
    
    
    def read_and_resize_image(self,image):
        start_t = time.time()
        img = cv2.imread(image)
        resized_image = cv2.resize(img, (self.width,self.height))
        gray = cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)
        to_read = np.array((gray.tolist()))
        gray[np.logical_and(gray>=self.skip_color_start,gray<= self.skip_color_end)]=255
        end_t = time.time() 
#         print("read_and_resize_image: "+str(end_t-start_t))
        return gray,resized_image,to_read
    
    
    def draw_segmented_rows(self,gray,primary,resized_image):
        start_t = time.time()
        row_vector=self.d3.calculate_vector(gray,False,0,0)
        horizontal_chunks_index=self.d3.primary_segmentation(gray,row_vector,primary)
        horizontal_chunks_index = self.d3.accumulate_whitespaces(horizontal_chunks_index)
        horizontal_chunks_index.append(self.height)
        end_t = time.time() 
#         print("draw_segmented_rows: "+str(end_t-start_t))
        return horizontal_chunks_index,row_vector,resized_image

    def draw_table_in_chunks(self,gray,secondary_vertical,secondary_horizontal,horizontal_chunks_index,row_vector,resized_image):
        start_t = time.time()
        height_index = 0
        data = []
        while height_index <= len(horizontal_chunks_index) - 2:
            inner_dict = {"start":0,"end":0,"columns":[],"rows":[]}
            start=height_index
            end=height_index+1
            start_index=horizontal_chunks_index[start]
            end_index=horizontal_chunks_index[end]
            inner_dict["start"] = start_index
            inner_dict["end"] = end_index
            column_vector=self.d3.calculate_vector(gray,True,start_index,end_index)
            inner_dict=self.d3.print_secondary_columns(column_vector,secondary_vertical,inner_dict)
            inner_dict=self.d3.print_secondary_rows(start_index,end_index,row_vector,secondary_horizontal,inner_dict) 
            height_index = end
            data.append(inner_dict)
        end_t = time.time() 
#         print("draw_table_in_chunks: "+str(end_t-start_t))
        return resized_image,data
    
    def display_image(self,image_name,window_name):
        start_t = time.time()
        cv2.imshow(window_name,image_name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        end_t = time.time()
#         print("display_image: "+str(end_t-start_t))







#level1
class data_chunking_level_1():

    
    def __init__(self,height,width,skip_color_start,skip_color_end):
        self.height=height
        self.width=width
        self.d2=data_chunking_level_2(height,width,skip_color_start,skip_color_end)
    
    def draw_row_chunks_on_image_file(self,image,primary):
        start_t = time.time()
        gray,resized_image,to_read=self.d2.read_and_resize_image(image)
        horizontal_chunks_index,row_vector,resized_image = self.d2.draw_segmented_rows(gray,primary,resized_image)
        end_t = time.time() 
#         print("draw_row_chunks_on_image_file: "+str(end_t-start_t))
        return horizontal_chunks_index,gray
    
    def draw_table_on_image_file(self,image,primary,secondary_vertical,secondary_horizontal):
        start_t = time.time()
        data_dict = {"height":0,"width":0,"chunk":[]}
        gray,resized_image,to_read=self.d2.read_and_resize_image(image)
        horizontal_chunks_index,row_vector,resized_image = self.d2.draw_segmented_rows(gray,primary,resized_image)
        resized_image,data = self.d2.draw_table_in_chunks(gray,secondary_vertical,secondary_horizontal,horizontal_chunks_index,row_vector,resized_image)
        data_dict["height"] = self.height
        data_dict["width"] = self.width 
        data_dict["chunk"] = data
        end_t = time.time()
        print("draw_table_on_image_file: "+str(end_t-start_t))
        return data_dict,horizontal_chunks_index,to_read
        

