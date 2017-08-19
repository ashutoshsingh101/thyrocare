import cv2
from google.cloud import vision
import io
import numpy as np
import time
import pytesseract
from PIL import Image

class optical_image_recognition():

    def __init__(self):
        pass

    def crop_image(self,gray,my_dict):
        start_t = time.time()
        vision_client = vision.Client()
        out=np.array(self.get_coordinates(my_dict))
        v = 0.0
        for primary_row in out:
            for secondary_column in primary_row:
                for secondary_row in secondary_column:
                    if type(secondary_row) is dict:
                        try:
                            crop = gray[int(secondary_row['y0']):int(secondary_row['y1']),int(secondary_row['x0']):int(secondary_row['x1'])].copy()
                        except TypeError:
                            continue
                        avg=np.mean(np.mean(crop))
                        if avg<255.0:
                            cv2.imwrite('image/crop/temp.png',crop)
                            image_file= io.open('image/crop/temp.png','rb')
                            content = image_file.read()
                            image = vision_client.image(content=content)
                            s = time.time()
                            want = image.detect_full_text()
                            e = time.time()
                            v= v+(e-s)
                            secondary_row['text']=want.text

			 #    if secondary_row['text'] == '':
				# #edges = cv2.Canny(crop,50,150,apertureSize = 3)
    #                             crop_thresh = cv2.threshold(crop, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #                             #kernel = np.ones((5,5), np.uint8)
    #                             #crop_thresh = cv2.erode(edges, kernel, iterations=1)
				# cv2.imwrite('image/crop/temp.png',crop_thresh)
    #   				image_file= io.open('image/crop/temp.png','rb')
    #                             content = image_file.read()
    #                             image = vision_client.image(content=content)
    #                             want = image.detect_full_text()
                                #secondary_row['text']=want.text
                            image_file.close()
        for i in range(len(out)):
            out[i]=np.transpose(out[i])
        end_t = time.time()
        print("crop_image: "+str(end_t-start_t))
        return out  

    def get_coordinates(self,my_dict):
        start_t = time.time()
        main_list = []
        for inner_dict in my_dict["chunk"]:
            inner_list = []
            if len(inner_dict["columns"]) > 0:
                column_list = inner_dict["columns"]
                x0 = 0
                for column in range(len(column_list)+1):
                    if column == len(column_list):
                        x1 = my_dict['width']
                        self.get_rows(inner_dict,inner_list,x0,x1)
                        break

                    else:
                        x1 = column_list[column]
                        if x1 != x0:
                            self.get_rows(inner_dict,inner_list,x0,x1)
                        x0 = x1 
            else:
                x0 = 0
                x1 = my_dict['width']
                val={'x0': x0,'x1':x1,'y0':inner_dict['start'],'y1':inner_dict['end'],'text':""}
                if val not in inner_list:
                    inner_list.append(val)
            main_list.append(inner_list)
        end_t = time.time()
        print("get_coordinates: "+str(end_t-start_t))
        return main_list 

    def get_rows(self,inner_dict,inner_list,x0,x1):
        start_t = time.time()
        if len(inner_dict["rows"]) > 0:
            row_list = inner_dict["rows"]
            y0 = inner_dict['start']
            deep_inner_list=[]
            for row in range(len(row_list)+1):
                if row == len(row_list):
                    y1 = inner_dict['end']
                    if deep_inner_list not in inner_list:
                        inner_list.append(deep_inner_list)
                    val={'x0': x0,'x1':x1,'y0':y0,'y1':y1,'text':""}
                    if val not in deep_inner_list:
                        deep_inner_list.append(val)
                    break

                else:
                    y1 = row_list[row]
                    if y1 != y0:
                        if deep_inner_list not in inner_list:
                            inner_list.append(deep_inner_list)
                        val={'x0': x0,'x1':x1,'y0':y0,'y1':y1,'text':""}
                        if val not in deep_inner_list:
                            deep_inner_list.append(val)
                    y0 = y1  
        else :
            deep_inner_list=[]
            if deep_inner_list not in inner_list:
                inner_list.append(deep_inner_list)
            val={'x0': x0,'x1':x1,'y0':inner_dict['start'],'y1':inner_dict['end'],'text':""}
            if val not in deep_inner_list:
                deep_inner_list.append(val)
        end_t = time.time()
        print("get_rows: "+str(end_t-start_t))
