from django.db import connection
from .functions import *

def get_trains(from_des,to_des,date,category):
    all_trains = None

    train_query = """
        call route_lookup('%s','%s','%s'); 
    """ % (from_des,to_des,date)

    all_trains=execute_sql(train_query)

    for train in all_trains:
        train["Seat_availability"] = get_seat_available(train["Route_id"],category)
        train["Start_station_details"] = get_station_details(train["Start_station_id"])
        train["End_station_details"] = get_station_details(train["End_station_id"])
        train["Train_name"] = get_train_name(train["Train_id"])
        train["category"] = category


    print(all_trains)
    return all_trains

def get_seat_available(route_id,category="NA"):
    available_table =  execute_sql("CALL seat_avail(%s)" %(route_id))
    
    Seat_availability = {}
    for row in available_table:
        Seat_availability[row["seat_class"]] = (row["available_seats"] - get_num_WL(route_id,row["seat_class"]),get_price(route_id,row["seat_class"],category))
    
    return Seat_availability


def confirm_booking(data,route_id,S_cls,category="NA"):
    query = """
        call insert_booking("%s","%s","%s","%s","%s",%s,"%s");
    """ % (data["name"],data["Phone_no"],"2005-10-10","ON",S_cls,route_id,category)

    return execute_sql(query)[0]

def cancel_booking(PNR):
    query = """
        call cancellation(%s);
    """% PNR

    message = execute_sql(query)[0]["Message"]

    if(message == "done"):
        return True
    else:
        return False
    
def get_user_pnr(PNR):
    query = """
        call PNR_details_to_user(%s);
    """% PNR

    return execute_sql(query)[0]


def get_passengers(train_id,date):
    query = """
    call  passenger_list(%s,"%s");
""" % (train_id,date)
    
    return execute_sql(query)

def get_wl_passengers(train_id,date):
    query = """
    call  list_passenger_wl(%s,"%s");
""" % (train_id,date)
    
    return execute_sql(query)

def get_refund_amount(route_id):
    query = """
    call  refund_amount(%s);
""" % (route_id)
    
    return execute_sql(query)

def get_revenue(from_date,to_date):
    query = """
    call  Revenue_over_time('%s','%s');
""" % (from_date,to_date)
    
    return execute_sql(query)[0]

def get_refunded_list():
    query = """
    call  cancellation_records();
"""
    return execute_sql(query)

def get_busiest_route():
    query = """
    call busy_routes();
"""
    return execute_sql(query)[0]


def get_train(train_id,date):
    train_query = """
    select * from rail_routes where train_id = %s and date(Start_time) = "%s";
""" % (train_id,date)
    print(train_query)
    all_trains=execute_sql(train_query)

    for train in all_trains:
        train["Start_station_details"] = get_station_details(train["Start_station_id"])
        train["End_station_details"] = get_station_details(train["End_station_id"])
        train["Seat_availability"] = get_seat_available(train["Route_id"])
        train["Train_name"] = get_train_name(train["Train_id"])

    print(all_trains)
    return all_trains