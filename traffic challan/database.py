import pymongo

def insert_data(number_plate, red_light, helmet, speeding, triple):
    return
#     # Connect to MongoDB
#     client = pymongo.MongoClient("mongodb+srv://Tejas:Tejasiyer%402003@cluster0.fzlpz3a.mongodb.net/")
    
#     # Choose or create a database
#     db = client['Cluster0']
    
#     # Choose or create a collection (analogous to a table in SQL)
#     traffic_data_collection = db['traffic_data']

#     # Check if a record with the given number plate already exists
#     existing_record = traffic_data_collection.find_one({'number_plate': number_plate})

#     if existing_record:
#         # If the record already exists, update the values
#         updated_red_light = existing_record.get('red_light', 0) + red_light
#         updated_helmet = existing_record.get('helmet', 0) + helmet
#         updated_speeding = existing_record.get('speeding', 0) + speeding
#         updated_triple = existing_record.get('triple', 0) + triple

#         update_query = {
#             '$set': {
#                 'red_light': updated_red_light,
#                 'helmet': updated_helmet,
#                 'speeding': updated_speeding,
#                 'triple': updated_triple
#             }
#         }

#         traffic_data_collection.update_one({'number_plate': number_plate}, update_query)
#     else:
#         # If the record does not exist, insert a new record
#         new_record = {
#             'number_plate': number_plate,
#             'red_light': red_light,
#             'helmet': helmet,
#             'speeding': speeding,
#             'triple': triple
#         }

#         traffic_data_collection.insert_one(new_record)

#     client.close()

