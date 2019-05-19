import logging
import azure.functions as func
import cv2
import tempfile
#from azure.storage.blob import (
#    BlockBlobService,
#    ContainerPermissions
#)
from datetime import datetime, timedelta
import io
from PIL import Image

def main(myblob: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes\n"
                 f"Blob URI: {myblob.uri}")

    theBytes = myblob.read()
    #logging.info(theBytes)

    #account_name ="user"
    #account_key ="key"
    #CONTAINER_NAME='container'

    tf = tempfile.NamedTemporaryFile()
    logging.info(tf.name)
    tf.write(theBytes)
    tf.seek(0)
    cap = cv2.VideoCapture(tf.name)
    logging.info(cap.isOpened())
    flag, frame = cap.read()
    if(flag):
        tf2 = tempfile.NamedTemporaryFile(mode = 'r+b',suffix='.jpg',delete=False)
        logging.info(tf2.name)
        cv2.imwrite(tf2.name,frame)
        img = Image.open(tf2.name)
        img_byte_arr = io.BytesIO()
        img.convert('RGB').save(img_byte_arr, format='JPEG')
        blobout.set(img_byte_arr.getvalue())

    tf.close()
    tf2.close()









    #block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

    #sas_url = block_blob_service.generate_container_shared_access_signature(
     #   CONTAINER_NAME,
     #   ContainerPermissions.WRITE,
     #   datetime.utcnow() + timedelta(hours=99),
     #   datetime.utcnow() + timedelta(hours=-99)
        
    #)

    #cv2Url = myblob.uri + '?' + sas_url
    #logging.info(cv2Url)

    #cap = cv2.VideoCapture(myblob.uri)
    #logging.info(cap.isOpened())
    #logging.info(myblob.uri)
    # take first frame of the video
    #pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    #while True:
    #    flag, frame = cap.read()
    #    if flag:
            # The frame is ready and already captured
           # #cv2.imshow('video', frame)
          #  pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
     #       logging.info("Acquired frame")
        #else:
         #   # The next frame is not ready, so we try to read it again
         #   cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        #    logging.info("frame is not ready")
       #     # It is better to wait for a while for the next frame to be ready
      #      cv2.waitKey(3000)

     #   if cv2.waitKey(10) == 27:
    #        break

    #cv2.imwrite('frame.jpg', frame)
    #img = Image.open('frame.jpg')
    #img_byte_arr = io.BytesIO()
    #img.convert('RGB').save(img_byte_arr, format='JPEG')

    
    
