_author_ = 'arichland'


import requests
import pymysql.cursors
import pydict


#MySQL connection fields
con = pymysql.connect(user = pydict.user,
                       password = pydict.password,
                       host = pydict.host,
                       database = pydict.database,
                       charset = pydict.charset)

def Linkedin_post():
    try:

     with con.cursor() as cur:
        #Get post from MySQL

        available = 'SELECT sum(case when  status = "Available" then 1 else 0 end) as Available FROM rtcaws01.tbl_Posts'
        cur.execute(available)
        rows_available = cur.fetchall()
        desc_available = cur.description
        print(f'{desc_available[0][0]:<1}')

        for row in rows_available:
            print(f'{row[0]}')
            available_count = row[0]

        if available_count == 0:

            #No more available posts, run update qry to rest all posts
            reset = 'Update tbl_Posts Set Status = "Available";'
            cur.execute(reset)

            #After updating posts, run select qry to find next post
            selectqry = 'Select Min(ID) as ID , LastPostUTC, Status, Title, URL, Descr FROM tbl_Posts where status = "Available"; '
            cur.execute(selectqry)

            rows = cur.fetchall()
            desc = cur.description
            print("\nSelect Query Result:")
            print(f'{desc[0][0]:<1} {desc[1][0]:<1} {desc[2][0]:<1} {desc[3][0]:<1} {desc[4][0]:<1} {desc[5][0]:<1}')

            #Assign record fields to variables
            for row in rows:
                print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {desc[5][0]:<1}')
                recordID = row[0]
                title = row[3]
                url = row[4]
                descr = row[5]

            #Run qry to update MySQL
            updateqry = "Update tbl_Posts set LastPostUTC = Now(), Status = 'Unavailable' where ID = %d" % (recordID)
            cur.execute(updateqry)

            selectqry2 = 'Select ID , LastPostUTC as Timestamp, Status, Title, URL, Descr FROM tbl_Posts where ID = %d' % (
                recordID)
            cur.execute(selectqry2)

            rows2 = cur.fetchall()
            desc2 = cur.description

            print("\nUpdate Query Result:")
            print(f'{desc2[0][0]:<1} {desc2[1][0]:<1} {desc2[2][0]:<1} {desc2[3][0]:<1} {desc2[4][0]:<1}, {desc2[5][0]:<1}')

            for row in rows2:
                print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}')

        else:

            selectqry = 'Select Min(ID) as ID , LastPostUTC, Status, Title, URL, Descr FROM tbl_Posts where status = "Available" '
            cur.execute(selectqry)

            rows = cur.fetchall()
            desc = cur.description
            print("\nSelect Query Result:")
            print(f'{desc[0][0]:<1} {desc[1][0]:<1} {desc[2][0]:<1} {desc[3][0]:<1} {desc[4][0]:<1} {desc[5][0]:<1}')

            # Assign record fields to variables
            for row in rows:
                print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {desc[5][0]:<1}')
                recordID = row[0]
                title = row[3]
                url = row[4]
                descr = row[5]

                # Run qry to update MySQL
                updateqry = "Update tbl_Posts set LastPostUTC = Now(), Status = 'Unavailable' where ID = %d" % (recordID)
                cur.execute(updateqry)
                selectqry2 = 'Select ID , LastPostUTC as Timestamp, Status, Title, URL, Descr FROM tbl_Posts where ID = %d' % (recordID)
                cur.execute(selectqry2)
                rows2 = cur.fetchall()
                desc2 = cur.description
                print("\nUpdate Query Result:")
                print(f'{desc2[0][0]:<1} {desc2[1][0]:<1} {desc2[2][0]:<1} {desc2[3][0]:<1} {desc2[4][0]:<1}, {desc2[5][0]:<1}')
                for row in rows2:
                    print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}')
    finally:
     con.commit()
     cur.close()
     con.close()

    # Post to LinkedIn
    access_token = pydict.token
    urn = pydict.member_id
    author = f"urn:li:person:{urn}"
    headers = {'X-Restli-Protocol-Version': '2.0.0',
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'}

    api_url_base = 'https://api.linkedin.com/v2/'
    api_url = f'{api_url_base}shares'

    post_data = {
    "content": {
        "contentEntities": [
            {
                "entityLocation": url,
                "thumbnails": [
                    {
                        "resolvedUrl": ""
                    }
                ]
            }
        ],
        "title": descr
    },
    "distribution": {
        "linkedInDistributionTarget": {}
    },
    "owner": author,
    "subject": title,
    "text": {
        "text": title
    }
}
    response = requests.post(api_url, headers=headers, json=post_data)
    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)
        print(api_url)

Linkedin_post()