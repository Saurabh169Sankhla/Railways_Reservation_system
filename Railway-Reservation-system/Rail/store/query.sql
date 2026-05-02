DELIMITER $$
CREATE PROCEDURE route_lookup(IN from_input VARCHAR(45),
IN to_input  VARCHAR(45),
in inp_date DATE)
BEGIN

    SELECT * FROM dbms.rail_routes where 
    Start_station_id IN 
        (SELECT id FROM dbms.rail_stations where District LIKE CONCAT(from_input, '%')) 
    AND 
    End_station_id IN 
        (SELECT id FROM dbms.rail_stations where District LIKE CONCAT(to_input, '%'))
    and DATE(Start_time) = inp_date;
    
END $$
DELIMITER ;



DELIMITER ;

DELIMITER $$
CREATE PROCEDURE seat_avail(IN in_route_no INT)
BEGIN
    SELECT seat_class, SUM(Available) AS available_seats 
    FROM rail_seats 
    WHERE Route_id = in_route_no and Booking_Status="CNF"
    GROUP BY seat_class;
END $$
 
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE insert_booking(
    IN u_name VARCHAR(30),
    IN u_phone VARCHAR(13),
    IN u_Dob DATE,
    IN t_payment VARCHAR(5),
    IN s_seat VARCHAR(6),
    IN Route_no INT,
    IN b_cat VARCHAR(5)
)
BEGIN
    DECLARE new_user_id INT;
    DECLARE new_transaction_id INT;
    DECLARE seat VARCHAR(6);
    DECLARE ticket_status VARCHAR(3);
    DECLARE done INT DEFAULT 0;
    DECLARE t_amount INT;
    DECLARE PNR INT;

    SELECT Taxable_value+ CGST+ CESS+ Route_id INTO t_amount FROM dbms.rail_ticket_price where Route_id=Route_no and Seat_class=s_seat;
    

    SET ticket_status = 'CNF';

    INSERT INTO rail_users (name, phone_no, DoB)
    VALUES (u_name, u_phone, u_Dob);
    SET new_user_id = LAST_INSERT_ID();

    INSERT INTO rail_transactions (Booking_date, Transaction_Amount, Payment_Method, Payment_Status)
    VALUES (NOW(), t_amount, t_payment, 'ok');
    SET new_transaction_id = LAST_INSERT_ID();

    IF NOT Exists(SELECT 1 FROM rail_seats WHERE Seat_class = s_seat AND Available = 1 and Route_id = Route_no LIMIT 1) THEN
		
        SET seat = "NA";
        SET ticket_status = 'WL';
    ELSE
        SELECT Seat_id INTO seat
		FROM rail_seats
		WHERE Seat_class = s_seat AND Available = 1 and Route_id = Route_no
		LIMIT 1;

        UPDATE rail_seats
        SET  Available = 0
        WHERE Seat_id = seat and Route_id = Route_no;
    END IF;

    INSERT INTO rail_bookings (Seat_no, Booking_Status, Booking_Catogory, Route_id, Transaction_id, user_id)
    VALUES (seat, ticket_status, b_cat, Route_no, new_transaction_id, new_user_id);
    SET PNR = LAST_INSERT_ID();

    SELECT PNR,ticket_status as Booking_Status,new_transaction_id as Transaction_id,t_amount as Transaction_Amount,b_cat as Booking_Catogory,seat as Seat_id;
END $$

DELIMITER ;



DELIMITER $$

CREATE PROCEDURE cancellation(IN in_booking_id INT)
BEGIN

DECLARE c_transaction_id INT;
DECLARE c_route_id INT;

IF (SELECT COUNT(*) FROM Bookings WHERE Booking_id =  in_booking_id) = 0 THEN
        SELECT 'Booking not found' AS Message;
ELSE

SELECT Route_id, Transaction_id INTO c_route_id, c_transaction_id FROM rail_bookings WHERE Booking_id =  in_booking_id;

UPDATE rail_bookings SET Booking_Status=’CNL’ WHERE Booking_id =  in_booking_id;

UPDATE rail_transactions SET Payment_Status=’RFN’ WHERE Transaction_id = c_transaction_id;

UPDATE rail_bookings SET Booking_Status = ‘CNF’ WHERE PNR = ( SELECT PNR FROM rail_bookings WHERE Route_id=c_route_id and Booking_Status LIKE ‘WTL’ LIMIT 1);

END IF;
END$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE PNR_details_to_user(IN pnr_no INT)
BEGIN
IF (SELECT COUNT(*) FROM rail_bookings WHERE PNR = pnr_no) > 0 
THEN
  -- User and booking details for all matching PNR rows
        SELECT 
            u.user_id,
            u.name,
            u.phone_no,
            b.Booking_Status,
            b.Booking_Catogory,
            b.Seat_no
        FROM 
            rail_bookings b
        JOIN 
            rail_users u ON b.user_id = u.user_id
        WHERE 
            b.PNR = pnr_no;
end if;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE passenger_list(IN train_id INT,in st_date DATE)
BEGIN
    SELECT 
        *
    FROM rail_bookings r
    JOIN rail_users u ON u.user_id = r.user_id
    Join rail_routes route on route.Route_id = r.Route_id 
    WHERE route.Train_id = train_id and date(route.Start_time) = st_date and Booking_Status="CNF";
END $$

DELIMITER ;


DELIMITER $$
CREATE PROCEDURE list_passenger_wl(IN train_id INT,in st_date DATE)
BEGIN
    SELECT 
        *
    FROM rail_bookings r
    JOIN rail_users u ON u.user_id = r.user_id
    Join rail_routes route on route.Route_id = r.Route_id 
    WHERE route.Train_id = train_id and date(route.Start_time) = st_date and Booking_Status="WL";
END $$

DELIMITER ;


DELIMITER $$
CREATE PROCEDURE Revenue_over_time(IN from_date DATE,IN to_date DATE)
BEGIN
	
	SELECT from_date as From_Date, to_date as To_Date,  IFNULL(SUM(Transaction_Amount),0) as Total_Revenue FROM rail_transactions where Booking_date BETWEEN from_date AND DATE_ADD(to_date,INTERVAL 1 DAY) and Payment_Status = 'ok';

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE busy_routes()
BEGIN
DECLARE route INT;
SELECT Route_id INTO route FROM rail_seats WHERE Available=0 GROUP BY Route_id ORDER BY COUNT(*) DESC LIMIT 1;

SELECT 
r.Train_id as Train_No,
tr.Train_name as Train_Name,
st1.Station_name as From_Station,
r.Start_time as Start_Time,
st2.Station_name as To_Station,
r.ENd_time as End_Time,
JOIN rail_trains tr ON r.Train_id=tr.Train_id,
JOIN rail_stations st1 ON r.Start_station_id=st1.id,
JOIN rail_stations st2 ON r.End_station_id=st2.id,
WHERE r.Route_id=route;

END $$
DELIMITER;


