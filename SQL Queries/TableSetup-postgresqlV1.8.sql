
ALTER TABLE public.players
    ADD COLUMN firstdetailupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN firstsummaryupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN lastdetailupdate timestamp without time zone;

    
ALTER TABLE public.players
    ADD COLUMN lastsummaryupdate timestamp without time zone;