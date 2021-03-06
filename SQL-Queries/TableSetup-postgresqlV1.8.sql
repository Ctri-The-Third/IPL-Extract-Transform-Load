
ALTER TABLE public.players
    ADD COLUMN firstdetailupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN firstsummaryupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN lastdetailupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN lastsummaryupdate timestamp without time zone;

    -- View: public."jobsView"

-- DROP VIEW public."jobsView";

CREATE OR REPLACE VIEW public."jobsView" AS
 WITH data AS (
         SELECT date_part('epoch'::text, now() - COALESCE(jobslist.lastheartbeat, jobslist.started)::timestamp with time zone) AS age,
            jobslist."desc",
            jobslist.id,
            jobslist.methodname,
            jobslist.started,
            jobslist.finished,
            jobslist.lastheartbeat,
            jobslist.resumeindex,
            jobslist.methodparams,
            jobslist.completeindex,
            count(j2.id) AS countofblocking
           FROM jobslist
             LEFT JOIN jobsblocking ON jobslist.id = jobsblocking.blockingid
             LEFT JOIN jobslist j2 ON j2.id = jobsblocking.jobid AND j2.finished IS NULL
          GROUP BY (date_part('epoch'::text, now() - COALESCE(jobslist.lastheartbeat, jobslist.started)::timestamp with time zone)), jobslist."desc", jobslist.id, jobslist.methodname, jobslist.started, jobslist.finished, jobslist.lastheartbeat, jobslist.resumeindex, jobslist.methodparams
        )
 SELECT
        CASE
            WHEN data.countofblocking::double precision > 0::double precision THEN 'blocked'::text
            WHEN data.age < 0::double precision THEN 'pending'::text
            WHEN data.age < 30::double precision AND data.finished IS NULL THEN 'alive'::text
            WHEN data.age < 120::double precision AND data.finished IS NULL THEN 'unhealthy'::text
            WHEN data.age > 120::double precision AND data.finished IS NULL THEN 'dead'::text
            WHEN data.age > 120::double precision AND data.finished IS NOT NULL THEN 'complete'::text
            WHEN data.finished IS NOT NULL THEN 'completing'::text
            ELSE NULL::text
        END AS healthstatus,
    data.age,
    data."desc",
    data.id,
    data.methodname,
    data.started,
    data.finished,
    data.lastheartbeat,
    data.resumeindex,
    data.methodparams,
        CASE
            WHEN data.finished IS NOT NULL THEN 100::numeric
            ELSE round((COALESCE(data.resumeindex::double precision, 0::double precision) / GREATEST(data.completeindex,1)::double precision * 100::double precision)::numeric, 4)
        END AS percenttocompletion,
    data.countofblocking
   FROM data
  ORDER BY data.started DESC;

ALTER TABLE public."jobsView"
    OWNER TO "LaserScraper";

