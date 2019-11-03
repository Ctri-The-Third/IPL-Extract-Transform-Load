from  WinCmdMenus import print_at
import SQLconnector

def queryAllJobs():
    conn = SQLconnector.connectToSource()
    cursor = conn.cursor()
    sql = """with data as ( 
	select row_number() over (partition by healthstatus order by finished desc ) as rowNo
	, * from public."jobsView"
    )
    select healthstatus, age, "desc", started,finished, percenttocompletion from data where rowNo < 5 or healthstatus != 'complete'"""

    cursor.execute(sql)
    return cursor.fetchall()


def renderJobs(jobslist):
    rowNo = 6
    for job in jobslist:
        print_at(rowNo,0,"%s\t %s,%s,%s") % (job[0],)
        print(job)
        rowNo = rowNo +1


renderJobs(queryAllJobs())
    