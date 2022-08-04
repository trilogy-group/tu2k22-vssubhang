## Instructions: Intro To Databases

# Setup
create database db_trial;
use db_trial;
create table company_info(company_code varchar(3), company_name varchar(30), comapny_email varchar(50), date Date NULL);
create table date_info(id int, date Date);
create table date_info(id int, date Date);
update date_info set date = DATE_ADD(NOW(), INTERVAL -id DAY);
alter table date_info drop column id;
create table stock_info as select * from company_info cross join date_info;
update stock_info set company_code = upper(substring(company_name, 1, 3));
alter table stock_info add column day_high float, add column day_low float, add column open float, add column close float, add column volume int;
update stock_info set volume = floor(1 + rand()*(200 - 1)), day_high = truncate(1 + rand()*(2000 - 1), 2), day_low = truncate(1 + rand()*(2000 - 1), 2);
update stock_info set day_high = day_high + day_low, day_low = day_high - day_low, day_high = day_high - day_low where day_high < day_low;
update stock_info set open = truncate(day_low + rand()*(day_high - day_low), 2), close = truncate(day_low + rand()*(day_high - day_low), 2);

# Queries

select company_name from (select (t1.close - t2.open)/ t2.open as growth, t1.company_name from stock_info t1 join stock_info t2 on t1.company_name = t2.company_name and t1.date = (select max(date) from stock_info) and t2.date = (select min(date) from stock_info)) as temp where growth = (select max((t1.close - t2.open)/ t2.open) from stock_info t1 join stock_info t2 on t1.company_name = t2.company_name and t1.date = (select max(date) from stock_info) and t2.date = (select min(date) from stock_info));
select company_name, avg((day_high - day_low)/day_low) as avg_volatility from stock_info group by company_name order by avg_volatility asc;
select company_name from (select (t1.close - t2.open)/ t2.open as growth, t1.company_name from stock_info t1 join stock_info t2 on t1.company_name = t2.company_name and t1.date = (select max(date) from stock_info) and t2.date = (date_add(date(now()), INTERVAL -30 DAY))) as temp where growth = (select min((t1.close - t2.open)/ t2.open) from stock_info t1 join stock_info t2 on t1.company_name = t2.company_name and t1.date = (select max(date) from stock_info) and t2.date = (date_add(date(now()), INTERVAL -30 DAY))));
select company_name from stock_info where (close * volume) in (select max(volume * close) from stock_info where date = date_add(date(now()), INTERVAL -70 DAY)) and date = date_add(date(now()), INTERVAL -70 DAY);
select date, avg((close - open) / open) as growth from stock_info t1 inner join (select company_name from stock_info where date = (select max(date) from stock_info) order by close * volume desc limit 5) t2 on t1.company_name = t2.company_name group by date order by growth desc limit 1;