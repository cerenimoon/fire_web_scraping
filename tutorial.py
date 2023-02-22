from selenium import webdriver
from selenium.webdriver.common.by import By 
import requests
import io
from PIL import Image
import time

path = "C:\\Users\\user\\Desktop\\archive_2\\webdriver\\chromedriver.exe"

wd = webdriver.Chrome(executable_path=path)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    #url = "https://www.google.com/search?q=wildfire+from+above&tbm=isch&ved=2ahUKEwj6ubWRo9v8AhU36rsIHTcuDpcQ2-cCegQIABAA&oq=wildfire+from+above&gs_lcp=CgNpbWcQAzIFCAAQgAQ6BAgAEEM6BggAEAcQHjoGCAAQCBAeOgcIABCABBAYOggIABAIEAcQHlDICVirK2CyMGgAcAB4AIABsAGIAfQFkgEDMC41mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=8jjNY_r4CrfU7_UPt9y4uAk&bih=722&biw=1536&hl=EN"
    url = "https://www.google.com/search?q=california+wildfires+2021&hl=EN&tbm=isch&sxsrf=AJOqlzXCvOn4HVl8XRB1ZqZ634lWbtU99A%3A1674495861559&source=hp&biw=1536&bih=722&ei=dcfOY9msH6uFxc8PrIGK0A0&iflsig=AK50M_UAAAAAY87VhebdbowDyd6bXjW_efunjkvOOlx9&oq=california+wild&gs_lcp=CgNpbWcQAxgDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoECCMQJzoHCCMQ6gIQJzoHCAAQgAQQE1AAWOQxYOdHaANwAHgAgAGFAYgB-hCSAQQwLjE4mAEAoAEBqgELZ3dzLXdpei1pbWewAQo&sclient=img"
    wd.get(url)

    image_urls = set()
    skips = 0
    while len(image_urls) + skips < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute("src") in image_urls:
                    max_images += 1
                    skips += 1
                    break
                if image.get_attribute("src") and "https" in image.get_attribute("src"):
                    image_urls.add(image.get_attribute("src"))
                    #download_image()
                    print(f"Found image {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content) #binary data
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
           image.save(f, "JPEG")

        print("Successful")
    except Exception as e:
        print("FAILED -", e)

#download_image("", image_url, "fire.jpg") #function

urls = get_images_from_google(wd, 2, 500)
print(urls)

for i, url in enumerate(urls):
    download_image("wildfire/", url, str(i) + "california" + ".jpg")
wd.quit()

