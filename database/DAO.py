from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(y1,y2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(c.constructorId), c.constructorRef, c.name, c.nationality
                    from constructors c, results r, races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId and r.`position` != 0 and ra.`year` >= %s and ra.`year` <= %s
                    order by c.constructorId asc"""

        cursor.execute(query, (y1,y2,))

        for row in cursor:
            costruttore = Constructor(
                row["constructorId"],
                row["constructorRef"],
                row["name"],
                row["nationality"],
                0
            )
            results.append(costruttore)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2, idMapD):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select d1.id as id1, d2.id as id2
                    from (select distinct(r.constructorId) as id,r.driverId as driver, c.name as name
                    from results r, races ra, constructors c 
                    where r.constructorId = c.constructorId and r.raceId = ra.raceId and r.`position` != 0 and ra.`year` >= %s and ra.`year` <= %s
                    order by r.driverId) d1,
                    (select distinct(r.constructorId) as id, r.driverId as driver, c.name as name
                    from results r, races ra, constructors c
                    where r.constructorId = c.constructorId and r.raceId = ra.raceId and r.`position` != 0 and ra.`year` >= %s and ra.`year` <= %s
                    order by r.driverId) d2
                    where d1.driver = d2.driver and d1.id > d2.id"""

        cursor.execute(query, (year1, year2, year1, year2,))

        for row in cursor:
            results.append(Arco(idMapD[row["id1"]], idMapD[row["id2"]]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVeterani(year1, year2, idMapD):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT r.constructorId as id, MIN(d.dob) as oldest_dob
                    FROM results r, races ra, drivers d
                    WHERE r.raceId = ra.raceId and r.driverId = d.driverId and ra.year >= %s AND ra.year <= %s AND r.position != 0
                    GROUP BY r.constructorId"""

        cursor.execute(query, (year1, year2, ))

        for row in cursor:
            results.append((idMapD[row["id"]], row["oldest_dob"]))

        cursor.close()
        conn.close()
        return results