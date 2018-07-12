# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
#
# chromedriver = "/Users/kylerood/Generic-Web-Classifier/chromedriver"
# browser = webdriver.Chrome(chromedriver)
# browser.get('https://images.google.com/')
#
# search = browser.find_element_by_name('q')
# search.send_keys("google search through python")
# search.send_keys(Keys.RETURN) # hit return after you enter search text
# time.sleep(5) # sleep for 5 seconds so you can see the results
#
# #execute scrolling on and infinite page
# SCROLL_PAUSE_TIME = 0.5
#
# # Get scroll height
# last_height = browser.execute_script("return document.body.scrollHeight")
#
# while True:
#     # Scroll down to bottom
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)
#
#     # Calculate new scroll height and compare with last scroll height
#     new_height = browser.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#
# #browser.execute_script(open("./grab_images.js").read())
# # js = "var script = document.createElement('script'); script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js'; document.getElementsByTagName('head')[0].appendChild(script); var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; }); var textToSave = urls.toArray().join('\n'); var hiddenElement = document.createElement('a'); hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave); hiddenElement.target = '_blank'; hiddenElement.download = 'urls.txt'; hiddenElement.click();"
# #
# # browser.execute_script(js)
#
# injected_javascript = (
#     "var script = document.createElement('script');"
#     "script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js';"
#     "document.getElementsByTagName('head')[0].appendChild(script);"
#     "var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; });"
#     "var textToSave = urls.toArray().join('\n');"
#     "var hiddenElement = document.createElement('a');"
#     "hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);"
#     "hiddenElement.target = '_blank';"
#     "hiddenElement.download = 'urls.txt';"
#     "hiddenElement.click();"
#
# )
#
# browser.execute_async_script(injected_javascript)
#
# #browser.quit()

from google_images_download import google_images_download
import os, errno
import time


def silent_remove_of_file(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
        return False
    return True


def test_download_images_to_default_location():
    start_time = time.time()
    arguments = {
        "keywords": "Polar bears",
        "limit": 5,
        "print_urls": True
    }
    try:
        temp = arguments['output_folder']
    except KeyError:
        pass
    else:
        assert False, "This test checks download to default location yet an output folder was provided"

    output_folder_path = os.path.join(os.path.realpath('.'), 'downloads', '{}'.format(arguments['keywords']))
    if os.path.exists(output_folder_path):
        start_amount_of_files_in_output_folder = len([name for name in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, name)) and os.path.getctime(os.path.join(output_folder_path, name)) < start_time])
    else:
        start_amount_of_files_in_output_folder = 0

    response = google_images_download.googleimagesdownload()
    response.download(arguments)
    files_modified_after_test_started = [name for name in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, name)) and os.path.getmtime(os.path.join(output_folder_path, name)) > start_time]
    end_amount_of_files_in_output_folder = len(files_modified_after_test_started)
    print(f"Files downloaded by test {__name__}:")
    for file in files_modified_after_test_started:
        print(os.path.join(output_folder_path, file))


    # assert end_amount_of_files_in_output_folder - start_amount_of_files_in_output_folder == argumnets['limit']
    assert end_amount_of_files_in_output_folder == arguments['limit']

    print(f"Cleaning up all files downloaded by test {__name__}...")
    for file in files_modified_after_test_started:
        if silent_remove_of_file(os.path.join(output_folder_path, file)):
            print(f"Deleted {os.path.join(output_folder_path, file)}")
        else:
            print(f"Failed to delete {os.path.join(output_folder_path, file)}")

test_download_images_to_default_location()
