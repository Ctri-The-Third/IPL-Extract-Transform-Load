from  WinCmdMenus import print_at,clearScreen
import SQLconnector
import time
def queryAllJobs():
    conn = SQLconnector.connectToSource()
    cursor = conn.cursor()
    sql = """with data as ( 
	select row_number() over (partition by healthstatus order by finished desc ) as rowNo
	, * from public."jobsView"
    )
    select healthstatus, age, "desc", to_char(started,'DD-Mon-YYYY HH24:MM') as started,finished, percenttocompletion from data where rowNo < 5 or healthstatus != 'complete'
    order by started desc, finished desc"""

    cursor.execute(sql)
    return cursor.fetchall()


def renderJobs(jobslist):
    rowNo = 6
    for job in jobslist:
        #print_at(rowNo,0,"%s\t %s\t,%s,%s" % (job[0], job[5], job[3], job[2]),PI=2)
        print_at(rowNo,0,"%s%s"[0:10] % (job[0]," "*10))
        outStr = "%s%s" % (job[5]," "*10)
        print_at(rowNo,11,outStr[0:6])
        print_at(rowNo,17,"%")

        print_at(rowNo,21,"%s"%job[3])

        outStr = "%s%s" % (job[2][0:40]," "*40)
        print_at(rowNo,41,outStr[0:40])
        #print(job)
        rowNo = rowNo +1

clearScreen()
while True:
    renderJobs(queryAllJobs())
    time.sleep(5)