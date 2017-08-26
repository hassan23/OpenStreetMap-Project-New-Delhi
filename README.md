# OpenStreetMap Data Wrangling with SQL

The location we are wrangling is **New Delhi** the capital city of India and the place currently I am living in.

I uses the [overpass api](http://overpass-api.de/query_form.html) to export the location data. My query is down below.

```
(node(28.6142,77.2023,28.6983,77.3767);
<;
);
out meta;
```

the output file name is **NewDelhi.osm** whose small sample is in the repository. 

# Auditing the OSM file

### 1. This step is performed to gather the general information about the tags. 

First we see how many different types of tags occurred how many times.

**Find the Code in:** tags_type.py

```
 member  : 10435
 meta    : 1
 nd      : 300875
 node    : 241026
 note    : 1
 osm     : 1
 relation: 603
 tag     : 61147
 way     : 47148
```

Then I categorized the tags who are name **tag** in three categories based on their key value.

* **lower:** The keys with lower characters.
* **lower_colon:** The keys with lower characters and colon **(:)**.
* **problemchars:** The keys with special characters like **#,$,@** etc.
* **others:**  the keys with rest of other types of values.

Then I check the occurrences of each type of key in tags. The result is below:

```
lower        : 59021 
lower_colon  : 2071
problemchars : 22
other        : 33
```

**2. In this step we see the problems we encountered in the osm file**

**Find the Code in:** tags_type.py

There are so many types of location to look up for auditing like **house no, street address, ameneties, shops.** I choose to audit street names as it needed so many corrections.

The first problem I found in many places the city name written in wrong format. So I updated it with the more suitable form.

**these are the two most common examples of that**
	
 * `delhi =>  Delhi`
	
 * `Delhi. => Delhi`

Another problem is names in hindi which may be difficult to understand for a non hindi speaker. So I updated it with their english meanings.

 * `Bagh =>  Park`
	
 * `Marg => Road`
 
 * `Chowk =>  Open Market`
	
 * `Bazaar => Market`
 
 * `Nagar => town`
 
 Then there are abbreviations which needed to be updated with the full word.
 
 * `Ln =>  Lane`
	
 * `Rd. => Road`
 
Then the words with lower cases and misspellings.

 * `cicus =>  Circle`
	
 * `lane => Lane`
 
 * `gate => Gate`
 
 
 # Cleaning the OSM file and load Into DB
 
 **Find the Code in:** data.py
 
 In this part I gather the data in a certain structure which is required to write in to a csv and then to DB.
 
 During the data structuring process I categorise the tags(tags/ways) in to three categories we make during auditing. 
 
 * **lower_colon:** The keys with lower characters and colon **(:)**.
 * **problemchars:** The keys with special characters like **#,$,@** etc.
 * **others:**  the keys with rest of other types of values.
 
 These categories are defined to give the tags a particular **type** and **key**. The **others** tags get categorised as **'regular'**.
 The **problemchars** tags will be ignored. The **lower_colon** tags gets the type the value before the colon(:) and key the value        before the colon(:).
 
 e.g. if key attribute in tag has value **add:street** then the type will be **add** and key will be **street**
 
 In the **lower_colon** tags , the values attributed will get updated based on the key it associated with.
 
  * If tags is of type street then we use the **audit.py** function **update_name** to update the street  name.
  * If tags is of type postcode the we check weather the postal code is a correct postal code or not.If the postcode is correct the it went as it is otherwise it went as 'null'.
  
  After Structuring the data We use the csv dictwrite to write into the **csvs** and then to **DB** as per the required schema.

# Data overview of files
```
NewDelhi.osm ......... 53.404 MB
NewDelhi.db .......... 28.490 MB
nodes.csv ............. 19.966 MB
nodes_tags.csv ........ 0.185 MB
ways.csv .............. 2.858 MB
ways_tags.csv ......... 1.801 MB
ways_nodes.cv ......... 7.346 MB  
```  
# SQL Queries

### No of unique users
```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
#### Output:
483

### No of Nodes:
```sql
sqlite> SELECT COUNT(*) FROM nodes;
```
#### Output:
241026

### No of Ways:
```sql
sqlite> SELECT COUNT(*) FROM ways;
```
#### Output:
47148
