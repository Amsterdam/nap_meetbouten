--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.meetbouten_referentiepuntmeting DROP CONSTRAINT meetbouten_referenti_meting_id_2334024f_fk_meetbouten_meting_id;
ALTER TABLE ONLY public.meetbouten_meting DROP CONSTRAINT meetbouten_metin_meetbout_id_5d9ceaae_fk_meetbouten_meetbout_id;
ALTER TABLE ONLY public.meetbouten_meetbout DROP CONSTRAINT meetbouten_meetbou_rollaag_id_1ec6a338_fk_meetbouten_rollaag_id;
ALTER TABLE ONLY public.meetbouten_referentiepuntmeting DROP CONSTRAINT meet_referentiepunt_id_05b1c098_fk_meetbouten_referentiepunt_id;
DROP INDEX public.nap_peilmerk_id_0d9d6c59_like;
DROP INDEX public.nap_peilmerk_geometrie_id;
DROP INDEX public.meetbouten_rollaag_geometrie_id;
DROP INDEX public.meetbouten_referentiepuntmeting_referentiepunt_id_05b1c098_like;
DROP INDEX public.meetbouten_referentiepuntmeting_meting_id_2334024f_like;
DROP INDEX public.meetbouten_referentiepuntmeting_f7ec7869;
DROP INDEX public.meetbouten_referentiepuntmeting_db75d4c2;
DROP INDEX public.meetbouten_referentiepunt_id_bd9b2bcc_like;
DROP INDEX public.meetbouten_referentiepunt_geometrie_id;
DROP INDEX public.meetbouten_meting_meetbout_id_5d9ceaae_like;
DROP INDEX public.meetbouten_meting_id_e8d56b53_like;
DROP INDEX public.meetbouten_meting_7aed37a6;
DROP INDEX public.meetbouten_meetbout_id_e8c83c8c_like;
DROP INDEX public.meetbouten_meetbout_geometrie_id;
DROP INDEX public.meetbouten_meetbout_b00d1a25;
ALTER TABLE ONLY public.nap_peilmerk DROP CONSTRAINT nap_peilmerk_pkey;
ALTER TABLE ONLY public.meetbouten_rollaag DROP CONSTRAINT meetbouten_rollaag_pkey;
ALTER TABLE ONLY public.meetbouten_referentiepuntmeting DROP CONSTRAINT meetbouten_referentiepuntmeting_pkey;
ALTER TABLE ONLY public.meetbouten_referentiepunt DROP CONSTRAINT meetbouten_referentiepunt_pkey;
ALTER TABLE ONLY public.meetbouten_meting DROP CONSTRAINT meetbouten_meting_pkey;
ALTER TABLE ONLY public.meetbouten_meetbout DROP CONSTRAINT meetbouten_meetbout_pkey;
ALTER TABLE public.meetbouten_referentiepuntmeting ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.meetbouten_rollaag;
DROP SEQUENCE public.meetbouten_referentiepuntmeting_id_seq;
DROP TABLE public.meetbouten_referentiepuntmeting;
DROP TABLE public.meetbouten_meting;
DROP VIEW public.geo_nap_peilmerk;
DROP TABLE public.nap_peilmerk;
DROP VIEW public.geo_meetbouten_referentiepunt;
DROP TABLE public.meetbouten_referentiepunt;
DROP VIEW public.geo_meetbouten_meetbout;
DROP TABLE public.meetbouten_meetbout;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: meetbouten_meetbout; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE meetbouten_meetbout (
    date_modified timestamp with time zone NOT NULL,
    id character varying(10) NOT NULL,
    buurt character varying(50),
    locatie_x numeric(10,2),
    locatie_y numeric(10,2),
    hoogte_nap numeric(7,4),
    zakking_cumulatief numeric(20,13),
    datum date,
    bouwblokzijde character varying(10),
    eigenaar character varying(50),
    beveiligd boolean,
    stadsdeel character varying(50),
    nabij_adres character varying(255),
    locatie character varying(50),
    zakkingssnelheid numeric(20,13),
    status character varying(1),
    bouwbloknummer character varying(4),
    blokeenheid smallint,
    geometrie geometry(Point,28992),
    rollaag_id integer
);


ALTER TABLE public.meetbouten_meetbout OWNER TO atlas_nap;

--
-- Name: geo_meetbouten_meetbout; Type: VIEW; Schema: public; Owner: atlas_nap
--

CREATE VIEW geo_meetbouten_meetbout AS
 SELECT mb.id,
    mb.id AS display,
    mb.status,
    mb.zakkingssnelheid,
    'meetbouten/meetbout' AS type,
    ((((site.domain)::text || 'meetbouten/meetbout/'::text) || (mb.id)::text) || '/'::text) AS uri,
    mb.geometrie
   FROM meetbouten_meetbout mb,
    django_site site
  WHERE (((site.name)::text = 'API Domain'::text) AND st_isvalid(mb.geometrie));


ALTER TABLE public.geo_meetbouten_meetbout OWNER TO atlas_nap;

--
-- Name: meetbouten_referentiepunt; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE meetbouten_referentiepunt (
    date_modified timestamp with time zone NOT NULL,
    id character varying(10) NOT NULL,
    locatie_x numeric(10,2),
    locatie_y numeric(10,2),
    hoogte_nap numeric(7,4),
    datum date,
    locatie character varying(255),
    geometrie geometry(Point,28992)
);


ALTER TABLE public.meetbouten_referentiepunt OWNER TO atlas_nap;

--
-- Name: geo_meetbouten_referentiepunt; Type: VIEW; Schema: public; Owner: atlas_nap
--

CREATE VIEW geo_meetbouten_referentiepunt AS
 SELECT rp.id,
    rp.id AS display,
    rp.hoogte_nap,
    'meetbouten/referentiepunt' AS type,
    ((((site.domain)::text || 'meetbouten/referentiepunt/'::text) || (rp.id)::text) || '/'::text) AS uri,
    rp.geometrie
   FROM meetbouten_referentiepunt rp,
    django_site site
  WHERE (((site.name)::text = 'API Domain'::text) AND st_isvalid(rp.geometrie));


ALTER TABLE public.geo_meetbouten_referentiepunt OWNER TO atlas_nap;

--
-- Name: nap_peilmerk; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE nap_peilmerk (
    date_modified timestamp with time zone NOT NULL,
    id character varying(10) NOT NULL,
    hoogte numeric(10,4),
    jaar integer,
    merk smallint,
    omschrijving text,
    windrichting character varying(2),
    muurvlak_x integer,
    muurvlak_y integer,
    geometrie geometry(Point,28992),
    rws_nummer character varying(10)
);


ALTER TABLE public.nap_peilmerk OWNER TO atlas_nap;

--
-- Name: geo_nap_peilmerk; Type: VIEW; Schema: public; Owner: atlas_nap
--

CREATE VIEW geo_nap_peilmerk AS
 SELECT pm.id,
    pm.id AS display,
    pm.hoogte,
    'nap/peilmerk' AS type,
    ((((site.domain)::text || 'nap/peilmerk/'::text) || (pm.id)::text) || '/'::text) AS uri,
    pm.geometrie
   FROM nap_peilmerk pm,
    django_site site
  WHERE (((site.name)::text = 'API Domain'::text) AND (pm.geometrie IS NOT NULL));


ALTER TABLE public.geo_nap_peilmerk OWNER TO atlas_nap;

--
-- Name: meetbouten_meting; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE meetbouten_meting (
    date_modified timestamp with time zone NOT NULL,
    id character varying(10) NOT NULL,
    datum date,
    type character varying(1),
    hoogte_nap numeric(7,4),
    zakking numeric(20,13),
    zakkingssnelheid numeric(20,13),
    zakking_cumulatief numeric(20,13),
    ploeg character varying(50) NOT NULL,
    type_int smallint,
    dagen_vorige_meting integer,
    pandmsl character varying(50),
    stadsdeel character varying(50),
    wvi character varying(50),
    meetbout_id character varying(10) NOT NULL
);


ALTER TABLE public.meetbouten_meting OWNER TO atlas_nap;

--
-- Name: meetbouten_referentiepuntmeting; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE meetbouten_referentiepuntmeting (
    id integer NOT NULL,
    meting_id character varying(10) NOT NULL,
    referentiepunt_id character varying(10) NOT NULL
);


ALTER TABLE public.meetbouten_referentiepuntmeting OWNER TO atlas_nap;

--
-- Name: meetbouten_referentiepuntmeting_id_seq; Type: SEQUENCE; Schema: public; Owner: atlas_nap
--

CREATE SEQUENCE meetbouten_referentiepuntmeting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetbouten_referentiepuntmeting_id_seq OWNER TO atlas_nap;

--
-- Name: meetbouten_referentiepuntmeting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: atlas_nap
--

ALTER SEQUENCE meetbouten_referentiepuntmeting_id_seq OWNED BY meetbouten_referentiepuntmeting.id;


--
-- Name: meetbouten_rollaag; Type: TABLE; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE TABLE meetbouten_rollaag (
    date_modified timestamp with time zone NOT NULL,
    id integer NOT NULL,
    locatie_x numeric(10,2),
    locatie_y numeric(10,2),
    geometrie geometry(Point,28992),
    bouwblok character varying(4)
);


ALTER TABLE public.meetbouten_rollaag OWNER TO atlas_nap;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: atlas_nap
--

ALTER TABLE ONLY meetbouten_referentiepuntmeting ALTER COLUMN id SET DEFAULT nextval('meetbouten_referentiepuntmeting_id_seq'::regclass);


--
-- Data for Name: meetbouten_meetbout; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY meetbouten_meetbout (date_modified, id, buurt, locatie_x, locatie_y, hoogte_nap, zakking_cumulatief, datum, bouwblokzijde, eigenaar, beveiligd, stadsdeel, nabij_adres, locatie, zakkingssnelheid, status, bouwbloknummer, blokeenheid, geometrie, rollaag_id) FROM stdin;
\.


--
-- Data for Name: meetbouten_meting; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY meetbouten_meting (date_modified, id, datum, type, hoogte_nap, zakking, zakkingssnelheid, zakking_cumulatief, ploeg, type_int, dagen_vorige_meting, pandmsl, stadsdeel, wvi, meetbout_id) FROM stdin;
\.


--
-- Data for Name: meetbouten_referentiepunt; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY meetbouten_referentiepunt (date_modified, id, locatie_x, locatie_y, hoogte_nap, datum, locatie, geometrie) FROM stdin;
\.


--
-- Data for Name: meetbouten_referentiepuntmeting; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY meetbouten_referentiepuntmeting (id, meting_id, referentiepunt_id) FROM stdin;
\.


--
-- Name: meetbouten_referentiepuntmeting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: atlas_nap
--

SELECT pg_catalog.setval('meetbouten_referentiepuntmeting_id_seq', 1, false);


--
-- Data for Name: meetbouten_rollaag; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY meetbouten_rollaag (date_modified, id, locatie_x, locatie_y, geometrie, bouwblok) FROM stdin;
\.


--
-- Data for Name: nap_peilmerk; Type: TABLE DATA; Schema: public; Owner: atlas_nap
--

COPY nap_peilmerk (date_modified, id, hoogte, jaar, merk, omschrijving, windrichting, muurvlak_x, muurvlak_y, geometrie, rws_nummer) FROM stdin;
\.


--
-- Name: meetbouten_meetbout_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY meetbouten_meetbout
    ADD CONSTRAINT meetbouten_meetbout_pkey PRIMARY KEY (id);


--
-- Name: meetbouten_meting_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY meetbouten_meting
    ADD CONSTRAINT meetbouten_meting_pkey PRIMARY KEY (id);


--
-- Name: meetbouten_referentiepunt_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY meetbouten_referentiepunt
    ADD CONSTRAINT meetbouten_referentiepunt_pkey PRIMARY KEY (id);


--
-- Name: meetbouten_referentiepuntmeting_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY meetbouten_referentiepuntmeting
    ADD CONSTRAINT meetbouten_referentiepuntmeting_pkey PRIMARY KEY (id);


--
-- Name: meetbouten_rollaag_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY meetbouten_rollaag
    ADD CONSTRAINT meetbouten_rollaag_pkey PRIMARY KEY (id);


--
-- Name: nap_peilmerk_pkey; Type: CONSTRAINT; Schema: public; Owner: atlas_nap; Tablespace: 
--

ALTER TABLE ONLY nap_peilmerk
    ADD CONSTRAINT nap_peilmerk_pkey PRIMARY KEY (id);


--
-- Name: meetbouten_meetbout_b00d1a25; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meetbout_b00d1a25 ON meetbouten_meetbout USING btree (rollaag_id);


--
-- Name: meetbouten_meetbout_geometrie_id; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meetbout_geometrie_id ON meetbouten_meetbout USING gist (geometrie);


--
-- Name: meetbouten_meetbout_id_e8c83c8c_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meetbout_id_e8c83c8c_like ON meetbouten_meetbout USING btree (id varchar_pattern_ops);


--
-- Name: meetbouten_meting_7aed37a6; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meting_7aed37a6 ON meetbouten_meting USING btree (meetbout_id);


--
-- Name: meetbouten_meting_id_e8d56b53_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meting_id_e8d56b53_like ON meetbouten_meting USING btree (id varchar_pattern_ops);


--
-- Name: meetbouten_meting_meetbout_id_5d9ceaae_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_meting_meetbout_id_5d9ceaae_like ON meetbouten_meting USING btree (meetbout_id varchar_pattern_ops);


--
-- Name: meetbouten_referentiepunt_geometrie_id; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepunt_geometrie_id ON meetbouten_referentiepunt USING gist (geometrie);


--
-- Name: meetbouten_referentiepunt_id_bd9b2bcc_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepunt_id_bd9b2bcc_like ON meetbouten_referentiepunt USING btree (id varchar_pattern_ops);


--
-- Name: meetbouten_referentiepuntmeting_db75d4c2; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepuntmeting_db75d4c2 ON meetbouten_referentiepuntmeting USING btree (referentiepunt_id);


--
-- Name: meetbouten_referentiepuntmeting_f7ec7869; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepuntmeting_f7ec7869 ON meetbouten_referentiepuntmeting USING btree (meting_id);


--
-- Name: meetbouten_referentiepuntmeting_meting_id_2334024f_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepuntmeting_meting_id_2334024f_like ON meetbouten_referentiepuntmeting USING btree (meting_id varchar_pattern_ops);


--
-- Name: meetbouten_referentiepuntmeting_referentiepunt_id_05b1c098_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_referentiepuntmeting_referentiepunt_id_05b1c098_like ON meetbouten_referentiepuntmeting USING btree (referentiepunt_id varchar_pattern_ops);


--
-- Name: meetbouten_rollaag_geometrie_id; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX meetbouten_rollaag_geometrie_id ON meetbouten_rollaag USING gist (geometrie);


--
-- Name: nap_peilmerk_geometrie_id; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX nap_peilmerk_geometrie_id ON nap_peilmerk USING gist (geometrie);


--
-- Name: nap_peilmerk_id_0d9d6c59_like; Type: INDEX; Schema: public; Owner: atlas_nap; Tablespace: 
--

CREATE INDEX nap_peilmerk_id_0d9d6c59_like ON nap_peilmerk USING btree (id varchar_pattern_ops);


--
-- Name: meet_referentiepunt_id_05b1c098_fk_meetbouten_referentiepunt_id; Type: FK CONSTRAINT; Schema: public; Owner: atlas_nap
--

ALTER TABLE ONLY meetbouten_referentiepuntmeting
    ADD CONSTRAINT meet_referentiepunt_id_05b1c098_fk_meetbouten_referentiepunt_id FOREIGN KEY (referentiepunt_id) REFERENCES meetbouten_referentiepunt(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetbouten_meetbou_rollaag_id_1ec6a338_fk_meetbouten_rollaag_id; Type: FK CONSTRAINT; Schema: public; Owner: atlas_nap
--

ALTER TABLE ONLY meetbouten_meetbout
    ADD CONSTRAINT meetbouten_meetbou_rollaag_id_1ec6a338_fk_meetbouten_rollaag_id FOREIGN KEY (rollaag_id) REFERENCES meetbouten_rollaag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetbouten_metin_meetbout_id_5d9ceaae_fk_meetbouten_meetbout_id; Type: FK CONSTRAINT; Schema: public; Owner: atlas_nap
--

ALTER TABLE ONLY meetbouten_meting
    ADD CONSTRAINT meetbouten_metin_meetbout_id_5d9ceaae_fk_meetbouten_meetbout_id FOREIGN KEY (meetbout_id) REFERENCES meetbouten_meetbout(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetbouten_referenti_meting_id_2334024f_fk_meetbouten_meting_id; Type: FK CONSTRAINT; Schema: public; Owner: atlas_nap
--

ALTER TABLE ONLY meetbouten_referentiepuntmeting
    ADD CONSTRAINT meetbouten_referenti_meting_id_2334024f_fk_meetbouten_meting_id FOREIGN KEY (meting_id) REFERENCES meetbouten_meting(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

