## Introduction to Database Review

# Milestone 1
https://docs.google.com/document/d/1_R1IgeBqnAyQNFBmuJy68669B3KfKZkfOL0uxsj9gOY/edit?usp=sharing

# Milestone 3
1. select sum(t1.volume) from sell_order t1 left join open_sell_order t2 on t1.open_sell_orders_id = t2.id and t2.stock_id = given_id and t1.date= given_date;
2.select sum(profit) from buy_sell_mapping t1 left join buy_order t2 on t1.buy_order_id = t2.id and t2.date = given_date left join open_buy_order t3 on t3.user_id = given_user 
3. select t1.name from stock t1 left join ohlcv t2 on t1.id = given_id and t2.stock_id = given_id and t2.date = now() left join ohlcv t3 on t3.date = date_add(date(now(), interval -1 month)) order by growth desc limit 5;
4. select avg_buy_price from portfolio where users_id = given_user and stock_id = given_stock;
5. select (t2.price - t1.avg_buy_price) * t1.volume as profit/loss from portfolio t1 left join stock t2 on t1.stock_id = t2.id and t1.user_id = given_user;
6. select t1.name from portfolio t4 stock t1 left join on t4.users_id = given_user and t1.id = t4.stock_id left join ohlcv t2 on t1.id = given_id and t2.stock_id = given_id and t2.date = now() left join ohlcv t3 on t3.date = date_add(date(now(), interval -1 month)) order by growth desc limit 1;

Bonus: 