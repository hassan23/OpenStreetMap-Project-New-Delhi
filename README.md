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
 'member'  : 10435
 'meta'    : 1
 'nd'      : 300875
 'node'    : 241026
 'note'    : 1
 'osm'     : 1
 'relation': 603
 'tag'     : 61147
 'way'     : 47148
```



