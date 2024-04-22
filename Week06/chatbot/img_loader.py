from PIL import Image
from loguru import logger


def get_images(docs):
    img_list = []
    for doc in docs:
        file_name = doc.name  # doc 객체의 이름을 파일 이름으로 사용
        if 'png' in file_name or 'jpg' in file_name or 'jpeg' in file_name:
            with open(file_name, "wb") as file:  # 파일을 doc.name으로 저장
                file.write(doc.getvalue())

                logger.info(f"Uploaded {file_name}")
                img = Image.open(file_name)
                img_list.append(img)

    return img_list
