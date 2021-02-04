"""
Created on Jul 29, 2016
Edited on Feb 02, 2021 (by ckdghk777@gmail.com)

@author: TYchoi
@edit : ckdghk77

webtoon_cut_counter.py counts the number of cuts that a webtoon episode contains.
This information can be used as the "length" information of each episode.

1) Fixed minor bugs (connection related bugs)
2) Modified cutting policy (more elaborate cut)

"""
from PIL import Image, ImageFilter, ImageDraw
from selenium import webdriver
import urllib.request
import numpy as np
import time
import os
import matplotlib.pyplot as plt

cut_num = 0

def define_non_white_region(total_img):
    """
    Defines non-white region : images locations

    Our cutting policy is as follows:
     1) Detecting edges.
     2) Read horizontal pixels of the edge-detected image through top to bottom. (see webtoon_cut_counter.py
       3-1) If (edge info =0 -> >0) ==> beginning of image
       3-2) elif (edge info >0 -> =0) ==> end of image

    Args:
        total_img : Appended image
    Returns:
        start_height_list, end_height_list
    """

    width_length, height_length = total_img.size

    edge_img = total_img.convert('L').filter(ImageFilter.FIND_EDGES);

    edge_pix = np.transpose(np.asarray(edge_img))/255.0;

    edge_pix[np.where(edge_pix < 0.1)] = 0.0;
    edge_pix[np.where(edge_pix >= 0.1)] = 1.0;

    is_scanning = False;
    start_height_list = []
    end_height_list = []

    for height in range(1, height_length-1) :

        edge_h_line = edge_pix[1:-1, height:min(height+30,height_length-1)];

        if np.sum(edge_h_line) == 0.0 :  # no edge detected + high color consistency
            if is_scanning == True :
                ## background start
                end_height_list.append(height);
                is_scanning = False;

        elif np.sum(edge_h_line) > 0.0 :
            if is_scanning == False :
                ## background_ end
                start_height_list.append(height);
                is_scanning = True

    if len(end_height_list) != len(start_height_list) :
        end_height_list.append(height_length-1);
    return start_height_list, end_height_list


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

    driver.set_page_load_timeout(30)
    driver.get(url)
    try :
        image_blocks = driver.find_element_by_css_selector('#toonLayer').find_elements_by_tag_name('img')
        for img_b in image_blocks :
            sample_url = img_b.get_attribute('src')
            if "001.jpg" in sample_url :
                sample_url = sample_url.replace('001.jpg','')
                break;
    except :
        return 0

    number_of_cuts = 0

    im_total = None;

    for i in range(1,len(image_blocks)):
        time.sleep(np.random.uniform(low=0.0, high=1.0));

        save_name = 'cutCounter/'+str(i)+'.jpg'
        number = '00' + str(i)
        if len(number) > 3:
            number = number[1:]
        img_url = sample_url+number+'.jpg'
        #reqUrl = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'});

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        urllib.request.install_opener(opener)

        retry_no = 30;

        while retry_no > 0 :  # re-try until success

            try :
                urllib.request.urlretrieve(img_url, save_name)
                break;
            except:
                retry_no-=1;
                time.sleep(np.random.uniform(low=0.5, high=3.0))

        if retry_no <= 0 :
            break;

        im = Image.open(save_name);

        if im_total is None:
            im_total = im;
        else:
            im_new = Image.new('RGB', (im_total.width, im_total.height + im.height));
            im_new.paste(im_total, (0,0));
            im_new.paste(im, (0,im_total.height));
            im_total = im_new

    non_white_start, non_white_end  = define_non_white_region(im_total)
    number_of_cuts += crop_image(im_total, non_white_start, non_white_end , webtoon_id, episode_number)

    return number_of_cuts

def crop_image(total_img, non_white_start, non_white_end, webtoon_id, episode_number):
    """
    Remove small cuts or simple colored cuts.

    Args:
        total_img : Appended image
        non_white_start : a list of height indices, where a image starts
        non_white_end : a list of height indices, where a image ends
        save_name : the name of an image file
        webtoon_id : a webtoon id
        episode_number : a webtoon episode number
    Returns:
        cut_num : the number of cuts that an image file has
    """

    global cut_num

    width_length, height_length = total_img.size
    folder_name = os.path.join("./splitted_images", webtoon_id + "_" + str(episode_number));
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for i in range(len(non_white_start)) :

        if non_white_end[i] - non_white_start[i] > 200:
            img_out = total_img.crop((0, non_white_start[i], width_length, non_white_end[i]));

            unique_color = np.unique(np.reshape(np.transpose(np.array(img_out)), [3, np.prod(img_out.size[-2:])]), axis=1).shape[
                1];

            uniq_rate = unique_color  / np.prod(img_out.size[-2:]);

            if uniq_rate < 0.05 or unique_color < 3:
                continue;

            img_out.save(os.path.join(folder_name,str(cut_num)+'.jpg'))
            time.sleep(0.5)
            cut_num += 1


    return cut_num
            