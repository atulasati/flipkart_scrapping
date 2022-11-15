import json
from bs4 import BeautifulSoup as bs


def get_product_data(response):
    soup = str(response.text)
    soup1 = bs(soup, 'html.parser')
    script = soup1.find_all('script')
    js = str(script[13].text).replace('window.__INITIAL_STATE__ = ','').replace('e}};','e}}')
    data_json = json.loads(js)
    asin,brand,title,pro_dsc,mrp,price,bullet_1,bullet_2,bullet_3,bullet_4,bullet_5,size,img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,pack_of,model_name,quantity,ideal_for,country_of_origin,application,model_number,manufacturer,Importer,packer,material,color,status,fabric , mapping= [""]*37

    reward = {
    "Product ID": asin,	
    "Brand": brand,	
    "Title": title,	
    "Product DSC": pro_dsc,	
    "MRP": mrp,
    "Selling Price": price,
    "Bullet Point 1": bullet_1,
    "Bullet Point 2": bullet_2,
    "Bullet Point 3": bullet_3,
    "Bullet Point 4": bullet_4,
    "Bullet Point 5": bullet_5,
    'Mapping':mapping,
    "Size": size,
    "Image 1" :img1,
    "Image 2" :img2,
    "Image 3":img3,
    "Image 4":img4,
    "Image 5":img5,
    "Image 6":img6,
    "Image 7":img7,
    "Image 8":img8,
    "Image 9":img9,
    "Image 10":img10,
    "Pack of" :pack_of,
    "Model Name":model_name,
    "Quantity": quantity,
    "Ideal For":ideal_for,
    "Country of Origin":country_of_origin,
    "Application Area":application, 
    "Model Number":model_number,
    "Manufacturer's Details": manufacturer,
    "Importer's Details": Importer,
    "Packer's Details":packer,	
    "Material": material,
    "Color":color,
    "Status":status
    }



    def get_title(response):
        try:
            title = data_json["pageDataV4"]["page"]["data"]["10002"][1]["widget"]["data"]["titleComponent"]["value"]["newTitle"]
        except:
            try:
                title = data_json["seoMeta"]["metadata"]["schema"][1]["itemListElement"][4]["item"]["name"]
            except:
                try:
                    title = data_json["pageDataV4"]["page"]["data"]["10003"][0]["widget"]["data"]["productBreadcrumbs"][4]["title"]
                except:
                    title = ''
        try:
            if not title:
                title = response.xpath('//span[@class="B_NuCI"]/text()').get()
        except Exception as err:
            print("title exe....................................",err)
            title = 'null'
        return title

    def get_pro_dsc(response):
        try:
            pro_dsc = ''
            main_p =  len(data_json["pageDataV4"]["page"]["data"]["10005"])
            for m in range(main_p):
                try:
                    pro_dsc = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{m}')]["widget"]["data"]["renderableComponents"][0]["value"]["text"].replace('<p>','').replace('</p>','').replace('<br><br>','').strip()
                except:
                    continue
        except:
            pro_dsc = ''

        try:
            if not pro_dsc: 
                pro_dsc = response.xpath('//div[@class="_1mXcCf RmoJUa"]/p/text()').get()
                if not pro_dsc:
                    pro_dsc = response.xpath('//div[@class="_1mXcCf RmoJUa"]/text()').get()
                    if not pro_dsc:
                        pro_dsc = response.xpath('//div[@class="_1AN87F"]/text()').get()
        except: 
            pro_dsc = ""
        return pro_dsc

    def get_brand(response):
        try:
            main_b = len(data_json["seoMeta"]["metadata"]["schema"])
            for i in range(main_b):
                try:
                    brand = data_json["seoMeta"]["metadata"]["schema"][int(f'{i}')]["brand"]['name']
                except:
                    continue
        except:
            try:
             brand = data_json["pageDataV4"]["page"]["data"]["10002"][1]["widget"]["data"]["titleComponent"]["value"]["superTitle"]
            except:
                brand = ''

        try:
            if not brand:
                brand = response.xpath('//span[@class="G6XhRU"]/text()').get()
                brand = brand.split("\xa0")[0]
                print("Brand 1:- ", brand)
                if not brand:
                    brand = response.xpath('//span[@class="B_NuCI"]/text()').get()
                    brand = brand.split(" ")[0]
                    print("Brand 2:- ", brand)
        except:
            try:
                brand = response.xpath('//span[@class="B_NuCI"]/text()').get()
                brand = brand.split(" ")[0]
                print("brand 3 :- ", brand)
                print("exception in brand")
            except:
                brand = ""
        return brand

    def get_mapping_url(response):
        try: 
            mapping = response.xpath('//a[@class="_2whKao"]/text()').extract()
            mapping = ">".join(mapping)
        except:
            mapping = "null"
        return mapping

    def get_mrp(response):
        try: mrp = response.xpath('//div[@class="_3I9_wc _2p6lqe"]/text()').extract()[1]
        except : mrp = 'null'
        return mrp
        
    def get_price(response):
        try:  price = response.xpath('//div[@class="_30jeq3 _16Jk6d"]/text()').extract()[-1]
        except: price = 'null'

        try:
            price = price.split("₹")[1]
        except:
            price = "null"
        return price 
  
    def get_img(response):
        selector = str(response.text).replace(" ","").replace("  ","").replace("   ","").replace("\n","").replace("\n\n","").replace("\n\n\n","")
        x= selector
        data = str(x)
        li1 = []
        imgs_srcs = data.split('"ORGANIC","url":"http://rukmini1.flixcart.com/image/{@width}/{@height}/')
        for i, img_data in enumerate(imgs_srcs):
            if i>0:
                prefix = "http://rukmini1.flixcart.com/image/720/720/"
                x1 = prefix+img_data.split("?")[0]
                li1.append(x1)
                print(prefix+img_data.split("?")[0])
        for i in range(1,11):
            try:
                if i<=len(li1):
                    reward[f"Image {i}"] = li1[i-1]
                else:
                    reward[f"Image {i}"] = 'null'
            except:
                reward[f"Image {i}"] = 'null'
    
    def get_bullet_points(response):
        try:
            bullet_1 = ''
            main_b = data_json["pageDataV4"]["page"]["data"]["10004"]
            for mb in range(len(main_b)):
                try:
                    bullet_1 = data_json["pageDataV4"]["page"]["data"]["10004"][int(f'{mb}')]["widget"]["data"]["highlights"]["value"]["text"]
                    reward["Bullet Point 1"] = bullet_1
                except:
                    continue          
        except:
            bullet_1 = ''

        try:
            if not reward["Bullet Point 1"]:
                reward["Bullet Point 1"] = response.xpath('//div[@class="_2418kt"]/ul/li/text()').extract()
        except: reward["Bullet Point 1"] = 'null'
            
        try: reward["Bullet Point 2"] = response.xpath('//div[@class="_1RLviY"]/span/span/text()').extract()
        except: reward["Bullet Point 2"] = 'null'

        try: reward["Bullet Point 3"] = response.xpath('//div[@class = "_2MJMLX"]/text()').extract()
        except: reward["Bullet Point 3"] = 'null'

    def get_country_origin():
        c_o_o_f = []
        c_o_o_v = []
        try:
            main_origin = len(data_json["pageDataV4"]["page"]["data"]["10005"])
            for ori in range(main_origin):
                try:
                    c_o_o = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"]#[1]['values']
                    for co in range(len(c_o_o)):
                        of = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"][int(f'{co}')]["key"]
                        c_o_o_f.append(of)
                        ov = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"][int(f'{co}')]['values']
                        c_o_o_v.append(ov)
                    
                except:
                    continue
        except:
            pass
        try:
            if not c_o_o_f:
                main_origin = len(data_json["pageDataV4"]["page"]["data"]["10006"])
                for ori in range(main_origin):
                    try:
                        c_o_o = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"]
                        for co in range(len(c_o_o)):
                            of = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"][int(f'{co}')]["key"]
                            c_o_o_f.append(of)
                            ov =  data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{ori}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["mappedCards"][int(f'{co}')]["values"]
                            c_o_o_v.append(ov)
                    except:
                        continue
        except:
            pass
        for key, value in zip(c_o_o_f,c_o_o_v):
            if 'country of origin' in key.lower().strip():
                reward["Country of Origin"] = value
    
       
    def get_product_details(data_json,response):
        size,pack_of,model_name,quantity,ideal_for,country_of_origin,application,model_number,manufacturer,Importer,packer,material,color,fabric,lehenga_fabric,choli_fabric= [""]*16
        product_keys = []
        product_values = []
        try:
            product_keys = []
            product_values = []
            main_l = len(data_json["pageDataV4"]["page"]["data"]["10005"])
            for le in range(main_l):
                try:
                    sp = len(data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{le}')]["widget"]["data"]["renderableComponents"])
                except:
                    continue
                for j in range(sp):
                    try:
                        nv = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{le}')]["widget"]["data"]["renderableComponents"][int(f'{j}')]["value"]['attributes']
                    except:
                        continue
                    for i in nv:
                        product_keys.append(f'{i["name"]}')
                        product_values.append(f'{i["values"]}'.replace("['",'').replace("']",''))
        except:
            pass
        try:
            if not product_keys:
                le = len(data_json["pageDataV4"]["page"]["data"]["10006"])
                for l in range(le):
                    try:
                        specifications = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{l}')]["widget"]["data"]["renderableComponent"]["value"]["specification"]
                    except:
                        continue
                    for specifi in specifications:
                        product_keys.append(f'{specifi["name"]}')
                        product_values.append(f'{specifi["values"]}'.replace("['",'').replace("']",''))
                print('data fetch from page')
        except:
            pass
        try:
            if not product_keys:
                print('errro in find from souece page')
                product_keys = response.xpath('//td[@class="_1hKmbr col col-3-12"]/text()').extract()
                product_values = response.xpath('//td[@class="URwL2w col col-9-12"]/ul/li/text()').extract()
                try:
                    if len(product_keys) == 0 and len(product_values) == 0:
                        product_keys = response.xpath('//div[@class="col col-3-12 _2H87wv"]/text()').extract()
                        product_values = response.xpath('//div[@class="col col-9-12 _2vZqPX"]/text()').extract()
                except:
                    pass
        except:
            pass
        
        for key,value in zip(product_keys, product_values):
            # try:
            #     reward[key] = value
            # except:
            #     pass
            if not size and "size" in key.lower().strip():
                size = value
                print("Size:- ", size)
            if not pack_of and "pack of" in key.lower().strip():
                pack_of = value
                print("Pack of:- ", pack_of)
            if not model_name and "model name" in key.lower().strip():
                model_name = value
                print("Model Name; ", model_name)
            if not color and "color" in key.lower().strip():
                color = value
                print("Color:- ", color)
            if not model_number and "model number" in key.lower().strip():
                model_number = value
                print("Model Number:- ", model_number)
            if not ideal_for and ('ideal for' or 'Ideal for') in key.lower().strip():
                ideal_for = value
                print("Ideal for:- ", ideal_for)
            if not country_of_origin and "country of origin" in key.lower().strip():
                country_of_origin = value
                print("Country of Origin:- ", country_of_origin)
            if not lehenga_fabric and "lehenga fabric" in key.lower().strip():
                lehenga_fabric = value
                print("Lehenga Fabric:-",lehenga_fabric)
            if not choli_fabric and "choli fabric" in key.lower().strip():
                choli_fabric = value
                print("Choli Fabric:-",choli_fabric)
            if not fabric and "fabric" in key.lower().strip():
                if (key.lower().strip()) != 'fabric care' :
                    material = value
                print("Fabric:-",material) 
            if material and "material" in key.lower().strip():
                material = value
                print("Material:-",material)
            if not quantity and "quantity" in key.lower().strip():
                quantity = value
                print("Quantity:-",quantity)
            

        reward['Size'] = size
        reward['Pack of'] = pack_of
        reward['Model Name'] = model_name
        reward['Color'] = color
        reward["Model Number"] = model_number
        reward["Ideal For"] = ideal_for
        reward["Country of Origin"] = get_country_origin()
        reward["Application Area"] = application
        reward["Manufacturer's Details"] = manufacturer
        reward["Importer's Details"] = Importer
        reward["Packer's Details"] = packer
        reward["Material"] = material
        reward["Quantity"] = quantity

        try:
            mat1 = f"{lehenga_fabric} {choli_fabric}"
        except:
            mat1 = "null"
        if not mat1:
            mat1 = fabric
        if not mat1:
            mat1 = material

        reward['Material'] = mat1 + material
   
    def get_application_area(responce):
        try:
            area = get_mapping_url(responce)
            try:
                area = area.split('>')[1]
            except:
                area = ''
        except:
            area = ""
        print("######",area,"############")
        return area

    # def get_manufacture_details():
        try:
            manufacturer = data_json["pageDataV4"]["page"]["data"]["10005"][2]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][0]["value"]["callouts"]
        except:
            try:
                manufacturer = data_json["pageDataV4"]["page"]["data"]["10005"][4]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][0]["value"]["callouts"]
            except:
                manufacturer = ''
        return manufacturer

    def get_manufactural_packer():
        fields = []
        values = []
        try:
            main_packer = len(data_json["pageDataV4"]["page"]["data"]["10005"])
            for mp in range(main_packer):
                try:
                    sec_packer = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"]
                    break
                except:
                    continue
            third_packer = len(sec_packer)
            for th in range(third_packer):
                try:
                    packer = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][int(f'{th}')]["value"]["callouts"]
                    values.append(packer)
                    packer_by = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][int(f'{th}')]["value"]["subTitle"]
                    fields.append(packer_by)
                except:
                    continue            
        except :
            pass

        try:
            if not fields and not values:
                try:
                    main_packer = len(data_json["pageDataV4"]["page"]["data"]["10006"])
                    for mp in range(main_packer):
                        try:
                            sec_packer = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"]
                            break
                        except:
                            continue
                    third_packer = len(sec_packer)
                    for th in range(third_packer):
                        try:
                            packer = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][int(f'{th}')]["value"]["callouts"]
                            values.append(packer)
                            packer_by = data_json["pageDataV4"]["page"]["data"]["10006"][int(f'{mp}')]["widget"]["data"]["listingManufacturerInfo"]["value"]["detailedComponents"][int(f'{th}')]["value"]["subTitle"]
                            fields.append(packer_by)
                        except:
                            continue   
                except:
                    pass         
        except :
            pass
                    
        for key, value in zip(fields,values):
            if 'manufactured by:' or 'manufactured by one of the following:' in key.lower().strip():
                reward["Manufacturer's Details"] = value
                print('--------------',value)
            if 'packed by:' or 'packed by one of the following:' in key.lower().strip():
                reward["Packer's Details"] = value
                print('--------------',value)
            if 'imported by:' or 'imported by one of the following:' in key.lower().strip():
                reward["Importer's Details"] = value
                print('--------------',value)

    def get_all_price(response):
        fields = []
        values = []
        main_v = len(data_json["pageDataV4"]["page"]["data"]["10005"])
        for mv in range(main_v):
            try:
                se_v = len(data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mv}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"])
            except:
                continue
            for sf in range(se_v):
                try:
                    f = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mv}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"][int(f'{sf}')]["priceType"]
                    fields.append(f)
    
                    v = data_json["pageDataV4"]["page"]["data"]["10005"][int(f'{mv}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"][int(f'{sf}')]["value"]
                    values.append(v)
                except:
                    continue 
        
        if not fields:
            try:
                mf = data_json["pageDataV4"]["page"]["data"]["ROOT"]
                for mff in range(len(mf)):
                    try:
                        sf = data_json["pageDataV4"]["page"]["data"]["ROOT"][int(f'{mff}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"]
                    except:
                        continue
                    for f in range(len(sf)):
                        try:
                            pf = data_json["pageDataV4"]["page"]["data"]["ROOT"][int(f'{mff}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"][int(f'{f}')]["priceType"]
                            fields.append(pf)
                            pv = data_json["pageDataV4"]["page"]["data"]["ROOT"][int(f'{mff}')]["widget"]["data"]["parentProduct"]["value"]["pricing"]["prices"][int(f'{f}')]["value"]
                            values.append(pv)
                        except:
                            continue
            except:
                pass
        
        if not fields:
            try:
                mf = data_json["pageDataV4"]["page"]["data"]["10002"]
                for mff in range(len(mf)):
                    try:
                        sf = data_json["pageDataV4"]["page"]["data"]["10002"][int(f'{mff}')]["widget"]["data"]["pricing"]["value"]["prices"]
                    except:
                        continue
                    for f in range(len(sf)):
                        try:
                            pf = data_json["pageDataV4"]["page"]["data"]["10002"][int(f'{mff}')]["widget"]["data"]["pricing"]["value"]["prices"][int(f'{f}')]["priceType"]
                            fields.append(pf)
                            pv = data_json["pageDataV4"]["page"]["data"]["10002"][int(f'{mff}')]["widget"]["data"]["pricing"]["value"]["prices"][int(f'{f}')]["value"]
                            values.append(pv)
                        except:
                            continue
            except:
                pass
        for key, value in zip(fields,values):
            if "MRP" in key:
                print(key,'----------------------------------------',value)
                reward["MRP"] = value
            if "FSP" in key:
                print(key,'----------------------------------------',value)
                reward["Selling Price"] = value

        if not reward["MRP"]:
            reward["MRP"] = get_mrp(response)
        if not reward["Selling Price"]:
            reward["Selling Price"] = get_price(response) 
        

    reward["Product ID"] = response.url.split("=")[1]
    reward["Title"] = get_title(response)
    reward["Product DSC"] = get_pro_dsc(response)
    reward['Brand'] = get_brand(response)
    reward['Mapping'] = get_mapping_url(response)
    get_all_price(response)
    get_product_details(data_json,response)
    reward["Application Area"] = get_application_area(response)
    get_country_origin()
    get_img(response)
    get_bullet_points(response)
    get_manufactural_packer()
    if reward['MRP'] == "null" and reward["Selling Price"] == "null":
        reward['Status'] = "Currently Unavailable"
    if reward['MRP'] == "null" and reward["Selling Price"] == "null" and not reward['Image 1'] and reward["Title"] == "null" and     reward['mapping'] == "null":
        reward['Status'] = "Error"

    return reward