import sys, csv, sqlite3
import requests

con = sqlite3.connect("../sqlite:///../db.sqlite3") # change to 'sqlite:///your_filename.db'
cur = con.cursor()



def main():
  cur.execute("SELECT * FROM web_movie ORDER BY id ASC")
  rows = cur.fetchall()
  l = len(rows)


  for i, row in enumerate(rows):
    try:
      print(str(i+1)+'/'+str(l))
      r =requests.get('https://image.tmdb.org/t/p/w500/'+row[3])
      if r.status_code == 404:
        r1 = requests.get('https://api.themoviedb.org/3/movie/'+str(row[0])+'?api_key=779122700619673300bd01d0d9b37fac')
        cur.execute("UPDATE web_movie SET poster_path = '"+r1.json()['poster_path']+"' WHERE id = "+str(row[0]))
        con.commit()
    except:
      print("An exception occurred: id="+str(row[0]))   
      cur.execute("DELETE FROM web_movie WHERE id = "+str(row[0])) 
      con.commit()

  con.close()


if __name__=='__main__':
    main()