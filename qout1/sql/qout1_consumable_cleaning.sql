select * from source
select * from project
select * from items
select * from type


select distinct description from items
where type = 'Consumables'
order by 1

--UPDATER
update items
set description = 'tig cleene (jar)'
where description = 'tig cleene' and unit = 'pcs'


update items
set unit = 'jar'
where unit = 'pcs' and description = 'tig cleene (jar)'

SELECT distinct description FROM items
where type = 'Consumables'
order by 1



SELECT description, unit_cost, unit, source FROM items
WHERE description LIKE '%een%'
order by 3


create view consumables_clean_table as
select * from items
where type = 'Consumables'

SELECT * FROM consumables_clean_table;
