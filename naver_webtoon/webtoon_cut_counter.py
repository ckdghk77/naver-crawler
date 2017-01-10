"""
Created on Jul 29, 2016

@author: TYchoi

webtoon_cut_counter.py counts the number of cuts that a webtoon episode contains.
This information can be used as the "length" information of each episode.
"""
from PIL import Image
from selenium import webdriver
import urllib.request
import time

cut_num = 0

def image_loader(name):
    """
    Loads a downloaded image

    Args:
        name: the name of image we want to load 
    Returns:
        height_length : the height of the image
        height_pix_list : the list of height indices that contains all white rows
    """
    
    im = Image.open(name)
    pix = im.load()       
    width_length, height_length = im.size
    height_pix_list = []
    for height in range(height_length):
        width_pix_list1 = []
        width_pix_list2 = []
        contains_non_white = False
        for width in range(width_length):
            try:
                r,g,b = pix[width,height]
            except:
                r,g,b,a = pix[width,height]
            if r > 240 and g > 240 and b >240:
                width_pix_list1.append(width)
            else:
                contains_non_white = True
            if contains_non_white:
                break
        if not contains_non_white:
            height_pix_list.append(height)
                
    return height_length, height_pix_list

def define_non_white_region(height_length, height_pix_list):
    """
    Defines non-white region : images locations 
    
    Args:
        height_length : the height of the image
        height_pix_list : the list of height indices that contains all white rows
    Returns:
        white_region : a list of height indices, where a image starts or ends
    """
        
    white_region = [0]
    for i in range(len(height_pix_list)-1):
        if height_pix_list[i+1]-height_pix_list[i] > 2:
            if height_pix_list[i] not in white_region:
                white_region.append(height_pix_list[i])
                white_region.append(height_pix_list[i+1])
    if len(white_region) % 2 == 1:
        white_region.append(height_pix_list[-1])
        
    if white_region[-1] == height_length-1:
        footer_ends_at = white_region[-2]
        white_region.remove(white_region[-1])
        white_region.remove(footer_ends_at)

    return white_region


def count_cuts(url, driver, webtoon_id, episode_number):
    """
    Counts the number of cuts (frames) within an episode 
    
    Args:
        url : an URL to a webtoon episode
        driver : a initialized webdriver
        webtoon_id : a webtoon id
        episode_number : a webtoon episode number
    Returns:
        number_of_cuts : the number of cuts that an episode has
    """

    driver.get(url)
    image_blocks = driver.find_element_by_css_selector('#toonLayer').find_elements_by_tag_name('img')
    sample_url = image_blocks[0].get_attribute('src').replace('001.jpg','')
    number_of_cuts = 0
    
    for i in range(1,len(image_blocks)-1):
        save_name = 'cutCounter/'+str(i)+'.jpg'
        number = '00' + str(i)
        if len(number) > 3:
            number = number[1:]
        img_url = sample_url+number+'.jpg'
        urllib.request.urlretrieve(img_url, save_name)
        height_length, height_pix_list = image_loader(save_name)
        try :
            white_region = define_non_white_region(height_length, height_pix_list)
            number_of_cuts += crop_image(white_region, save_name, webtoon_id, episode_number)
        except:
            number_of_cuts += 0
        break

    return number_of_cuts

def crop_image(white_region, save_name,webtoon_id, episode_number):
    """
    Crops an large image that contains multiple cuts into individual cuts. 
    
    Args:
        white_region : a list of height indices, where a image starts or ends
        save_name : the name of an image file
        webtoon_id : a webtoon id
        episode_number : a webtoon episode number
    Returns:
        cut_num : the number of cuts that an image file has
    """
    
    global cut_num
    im2 = Image.open(save_name)
    pix = im2.load()       
    width_length2, height_length2 = im2.size
    current_pos = 1
            
    for i in range(1,len(white_region)-1):
        if white_region[i+1] - white_region[i] > 100:
            im2.crop((0,white_region[i],width_length2,white_region[i+1])).save('splitted_images/'+webtoon_id+str(episode_number)+str(cut_num)+'.jpg')
            time.sleep(0.5)
            cut_num += 1
    return cut_num
            