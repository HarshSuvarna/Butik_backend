from google.cloud import storage
import os
import asyncio
import base64

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'src/dvastra-a063d-5cb3f873e3f6.json'
storage_client = storage.Client()

def uploadToBucket_stores(storeId, base64Str):
    blobName = 'storeImages/'+'store_'+str(storeId)[:8]+'_image'
    try:
        base64Str=base64.b64decode(base64Str)
        bucket = storage_client.get_bucket('dvastra_images')
        blob = bucket.blob(blobName)
        blob.cache_control = 'private'
        blob.upload_from_string(base64Str,content_type="image/jpg")
        imageUrl = 'https://storage.googleapis.com/dvastra_images/'+'storeImages/'+'store_'+str(storeId)[:8]+'_image'
       #print(imageUrl, 'inside funtion')
        return imageUrl
    except Exception as e:
       #print(e)
        return False 

def uploadToBucket_products(Id, base64Str):
    blobName = 'productImages/'+'product_'+str(Id)[:8]+'_image'
    try:
        base64Str=base64.b64decode(base64Str)
        bucket = storage_client.get_bucket('dvastra_images')
        blob = bucket.blob(blobName)
        blob.cache_control = 'private'
        blob.upload_from_string(base64Str,content_type="image/jpg")
        imageUrl = 'https://storage.googleapis.com/dvastra_images/'+'productImages/'+'product_'+str(Id)[:8]+'_image'
        return imageUrl
    except Exception as e:
       #print(e)
        return False 

def uploadToBucket_variants(Id, i, base64Str):
    blobName = 'variantImages/'+'variant_'+str(Id)[:8]+str(i)+'_image'
    try:
        base64Str=base64.b64decode(base64Str)
        bucket = storage_client.get_bucket('dvastra_images')
        blob = bucket.blob(blobName)
        blob.cache_control = 'private'
        blob.upload_from_string(base64Str,content_type="image/jpg")
        imageUrl = 'https://storage.googleapis.com/dvastra_images/'+'variantImages/'+'variant_'+str(Id)[:8]+str(i)+'_image'
       #print(imageUrl, 'inside functon')
        return imageUrl
    except Exception as e:
       #print(e)
        return "Image not uploaded"


def deleteImages(id, path):
    bucket = storage_client.get_bucket('dvastra_images')
    blobName = path + str(id)[:8]+'_image'
    blob = bucket.blob(blobName)
    blob.delete()
    return 'image deleted'

def deleteVariantImgs(id, length):
    bucket = storage_client.get_bucket('dvastra_images')
    for i in range(int(length)):
        blob = bucket.blob('variantImages/variant_' + str(id)[:8]+str(i)+'_image')
        blob.delete()
    return "image delted successfully"