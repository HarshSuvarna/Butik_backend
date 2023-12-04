# import uuid

# id = uuid.uuid5(uuid.NAMESPACE_DNS,'HARSH')

# stores = [(9,'afd',43),(9,'afd',43),(9,'afd',43),(9,'afd',43)]
# ss = (3,2,4,5)
# dd = ['44','4dsd','4wr','r3','sdfa']
# #for i in range(len(stores)):
#     #print(i+1)

# sqpList = [{'size':'3','price':344,'quantity':7}]
##print(type(sqpList[0]['price']))

# product_q = [('451387ba-8aa8-484c-afe5-19cac87a4e71', 'Trousers', 'vaafeffefdsssddsafsa', 'Addidas'), 
# ('bcb745e6-b64c-4f3a-bc6f-4b076347f5aa', 'Bata', 'rf34fqfwsdfsdfadfadsafdsddsdasfqwfwfqwf', 'Addidas'), 
# ('d4454001-155a-488b-8170-1132647a4375', 'Sandals', 'asdfsadrrffdfasfasdfsdfwff', 'Bata'), 
# ('e0af59a2-7ac6-468e-89bb-f5a52e5d1a50', 'Jordans', 'rf34fqfwsddsdasfqwfwfqwf', 'Addidas'), 
# ('e714f948-4942-48f6-adc0-4ecfa6bf3631', 'Jeans', 'ddd', 'Puma')]  

# variant_q  = [('451387ba-8aa8-484c-afe5-19cac87a4e71', '322'), 
# ('bcb745e6-b64c-4f3a-bc6f-4b076347f5aa', '211'), 
# ('d4454001-155a-488b-8170-1132647a4375', '211')]

# outputList =[]
#             #product_att = ['productId', 'title', 'imageUrl', 'price_min'] 
                    
# for product in product_q:                              #does not return those products whos variant are not made
#     for i in range(len(variant_q)):
#         if product[0] != variant_q[i][0]:
#             #print(product[0],'#')
#             #print(variant_q[i][0],'#')
#             continue
#         else:
#            #print(variant_q[i][0],'@')
#            #print(product[0],'@')

#             #print('**')
#             products = {'id':product[0], 'title':product[1], 'image_url':product[2], 'brand':product[3], 'price_min':variant_q[i][1]}
#             outputList.append(products)
#             break
    
##print(outputList)





# n =0
# while n !='x':
#     n = int(input('Enter an number: '))
#     mylist = [x for x in range(n+1) if x%2==1]
#     mylist.sort(reverse=True)
#    #print(mylist)
#     count=0
#     for k in mylist:
#        #print(' '*count,'*'*k)
#         count+=1

# d = 1
# dic = {'one':str(d)+' results found','two':2, 'three':3}
# #dic['one']=6
##print(dic['one'])

# from PIL import Image

# img = Image.open(r"test.jpg")
# img.tobytes('xbm', 'rgb')
##print(type(img))

# Code to convert img to base64 string
# import base64

# with open("test.jpg", "rb") as img_file:
#     b64_string = base64.b64encode(img_file.read())
#     with write("test_base64.txt", "rb") as txt_file_base64:
#         txt_file_base64.write(b64_string.decode('utf-8'))
##print(b64_string.decode('utf-8'))

# # Code to convert base64 to img
# import base64
# image = open('my_base64_imgdata.txt', 'rb')
# image_read = image.read()
# image_64_encode = base64.encodestring(image_read)
# image_64_decode = base64.decodestring(image_64_encode) 
# image_result = open('deer_decode.gif', 'wb') # create a writable image and write the decoding result
# image_result.write(image_64_decode)



# 1. Raju will give the image in base64.
# 2. Configure post request to take base64 string as input, convert back to img in api code and then store in google cloud storage in .jpg format.
# 3. Configure get request to provide "Google Cloud URL" of the img in response wherever applicable. -- easy



# import base64

# with open("testimg.jpg", 'rb') as img_file:
#     my_string = base64.b64encode(img_file.read())

##print(my_string)

# my_data= my_string

# with open("imageToSave.png", "wb") as img:
#     img.write(base64.decodebytes(my_data))

# stringds = 'https://storage.googleapis.com/dvastra_images/productImages/product_1206c8e6_image'
##print(len(stringds))

# str2 = 'asdfgh'
# str3 = 'asdfgh'

# if str2==str3:
#    #print('same')
# else:
#    #print('not same')

add = [
    {
      "productId": "87109c5f-7b02-4fa5-9d47-c1b32d55f011",
      "variantId": "30655280-ceb2-415e-8ca6-d3fa553a4683",
      "color": "Aero blue",
      "brandName": "Adidas",
      "material": "Aba",
      "categoryName": "Top wear",
      "subcategoryName": "Sneakers",
      "gender": "Unisex",
      "spq": [
        {
          "size": "UK 4.5",
          "price": 499,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 500,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 650,
          "quantity": 12
        }
      ],
      "images": [
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552802_image",
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552801_image"
      ]
    },
    {
      "productId": "87109c5f-7b02-4fa5-9d47-c1b32d55f011",
      "variantId": "30655280-ceb2-415e-8ca6-d3fa553a4683",
      "color": "Aero blue",
      "brandName": "Adidas",
      "material": "Aba",
      "categoryName": "Top wear",
      "subcategoryName": "Sneakers",
      "gender": "Unisex",
      "spq": [
        {
          "size": "UK 4.5",
          "price": 499,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 500,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 650,
          "quantity": 12
        }
      ],
      "images": [
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552802_image",
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552801_image"
      ]
    },
    {
      "productId": "87109c5f-7b02-4fa5-9d47-c1b32d55f011",
      "variantId": "30655280-ceb2-415e-8ca6-d3fa553a4683",
      "color": "Aero blue",
      "brandName": "Adidas",
      "material": "Aba",
      "categoryName": "Top wear",
      "subcategoryName": "Sneakers",
      "gender": "Unisex",
      "spq": [
        {
          "size": "UK 4.5",
          "price": 499,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 500,
          "quantity": 12
        },
        {
          "size": "UK 4.5",
          "price": 650,
          "quantity": 12
        }
      ],
      "images": [
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552802_image",
        "https://storage.googleapis.com/dvastra_images/variantImages/variant_306552801_image"
      ]
    }
  ]
lss = [3,4,5,6]
##print(len(add[0]["spq"][0]))

add[0]["spq"] = lss

print(add)