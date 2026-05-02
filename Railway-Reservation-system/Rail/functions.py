from django.db import connection

def get_train_id(ids):
    s = ','.join([str(x["id"]) for x in ids])
    
    print(s)  # 1
    return s

def execute_sql(query):
    out = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        out=dictfetchall(cursor)
    return out

def pnr_exist(PNR):
    query = """
        select exists(select * from rail_bookings where PNR= %s) as exist;
    """% PNR
    if(execute_sql(query)[0]["exist"] == 1):
        return True
    else:
        return False
    
def get_routid_pnr(PNR):
    query = """
    select route_id from rail_bookings where PNR= %s;
    """% PNR
    return execute_sql(query)[0]["route_id"]

def get_booking_details(PNR):
    query = """
        SELECT PNR,Booking_Status,Transaction_id,Booking_Catogory,Seat_no as Seat_id,user_id from rail_bookings where PNR = %s;            
""" % PNR
    return execute_sql(query)[0]

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    if cursor.description == None:
        return []
    
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_num_WL(route_id,S_class):
    query = """
    SELECT count(*) as total FROM dbms.rail_bookings where Booking_Status="WL" and Route_id = %s and Seat_no like '%s%%';
    """ % (route_id,S_class)
    print(query)
    return execute_sql(query)[0]["total"]

def get_price(route_id,S_cls,category="NA"):
    query = """
        SELECT Taxable_value as price FROM dbms.rail_ticket_price where Route_id=%s and Seat_class="%s";
    """ % (route_id,S_cls)
    price = execute_sql(query)[0]["price"]
    if category=='SEC':
        price = (price*80)//100
    elif category=="STD":
        price = (price*70)//100

    print(category,price)

    return price

def get_station_details(id):
    query = "SELECT Station_name ,District from dbms.rail_stations where id = %s ;" % id
    station = execute_sql(query)
    if len(station)==0:
        return ""
    return station[0]

def get_train_name(train_id):
    query = "SELECT Train_name from dbms.rail_trains where Train_id = %s ;" % train_id
    station = execute_sql(query)
    if len(station)==0:
        return ""
    return station[0]["Train_name"]

def route_not_exit(route_id):
    query = "SELECT count(*) as cnt from dbms.rail_routes where Route_id = %s ;" % route_id
    station = execute_sql(query)
    if station[0]["cnt"] == 1:
        return False
    else:
        return True
    
def seats_not_exist(route_id,S_cls):
    query = "SELECT count(*) as cnt from dbms.rail_seats where Route_id = %s and Seat_class = '%s';" % (route_id,S_cls)
    seats = execute_sql(query)
    if seats[0]["cnt"] == 0:
        return True
    else:
        return False
    
def get_ticket_details(route_id,S_cls='SL',category="NA"):
    train_query = """
        SELECT * FROM dbms.rail_routes where Route_id = %s ;
    """ % route_id

    query_output=execute_sql(train_query)
    train_details = {}

    if len(query_output) != 1:
        return train_details
    
    train_details = query_output[0]
    train_details["Start_station_details"] = get_station_details(train_details["Start_station_id"])
    train_details["End_station_details"] = get_station_details(train_details["End_station_id"])
    train_details["bill"] = get_bill(route_id,S_cls,category)
    train_details["category"] = category
    train_details["Train_name"] = get_train_name(train_details["Train_id"])

    return train_details

def get_bill(route_id,S_cls,category="NA"):
    query = """
        SELECT Seat_class, Taxable_value, CGST, CESS, Taxable_value+ CGST+ CESS+ Route_id as total FROM dbms.rail_ticket_price where Route_id=%s and Seat_class="%s";
    """ % (route_id,S_cls)

    price = {}
    output = execute_sql(query)

    if len(output)!=0:
        price = output[0]
    else:
        return price

    if category=='SEC':
        price["discount"] = (price["Taxable_value"]*20)//100
    elif category=="STD":
        price["discount"] = (price["Taxable_value"]*30)//100
    else :
        price["discount"] = 0

    price["total"] -= price["discount"]
    return price