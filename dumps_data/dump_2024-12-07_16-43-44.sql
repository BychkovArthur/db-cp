--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Debian 17.2-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: battle_record; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_record (
    id integer NOT NULL,
    subscribe_id integer NOT NULL,
    user1_score integer NOT NULL,
    user2_score integer NOT NULL,
    user1_get_crowns integer NOT NULL,
    user2_get_crowns integer NOT NULL,
    user1_card_ids integer[] NOT NULL,
    user2_card_ids integer[] NOT NULL,
    replay text,
    "time" timestamp without time zone NOT NULL,
    winner_id integer NOT NULL
);


ALTER TABLE public.battle_record OWNER TO postgres;

--
-- Name: battle_record_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.battle_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.battle_record_id_seq OWNER TO postgres;

--
-- Name: battle_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.battle_record_id_seq OWNED BY public.battle_record.id;


--
-- Name: battle_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.battle_type (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.battle_type OWNER TO postgres;

--
-- Name: battle_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.battle_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.battle_type_id_seq OWNER TO postgres;

--
-- Name: battle_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.battle_type_id_seq OWNED BY public.battle_type.id;


--
-- Name: card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.card (
    id integer NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    level integer NOT NULL
);


ALTER TABLE public.card OWNER TO postgres;

--
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.card_id_seq OWNER TO postgres;

--
-- Name: card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.card_id_seq OWNED BY public.card.id;


--
-- Name: clan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clan (
    id integer NOT NULL,
    tag text NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.clan OWNER TO postgres;

--
-- Name: clan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clan_id_seq OWNER TO postgres;

--
-- Name: clan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clan_id_seq OWNED BY public.clan.id;


--
-- Name: subscribe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscribe (
    id integer NOT NULL,
    user_id1 integer NOT NULL,
    user_id2 integer NOT NULL,
    battle_type_id integer NOT NULL
);


ALTER TABLE public.subscribe OWNER TO postgres;

--
-- Name: subscribe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscribe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscribe_id_seq OWNER TO postgres;

--
-- Name: subscribe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscribe_id_seq OWNED BY public.subscribe.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    tag text NOT NULL,
    is_super_user boolean NOT NULL,
    user_detailed_info_id integer NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_detailed_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_detailed_info (
    id integer NOT NULL,
    crowns integer NOT NULL,
    max_crowns integer NOT NULL,
    clan_id integer
);


ALTER TABLE public.user_detailed_info OWNER TO postgres;

--
-- Name: user_detailed_info_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_detailed_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_detailed_info_id_seq OWNER TO postgres;

--
-- Name: user_detailed_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_detailed_info_id_seq OWNED BY public.user_detailed_info.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: battle_record id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_record ALTER COLUMN id SET DEFAULT nextval('public.battle_record_id_seq'::regclass);


--
-- Name: battle_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_type ALTER COLUMN id SET DEFAULT nextval('public.battle_type_id_seq'::regclass);


--
-- Name: card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card ALTER COLUMN id SET DEFAULT nextval('public.card_id_seq'::regclass);


--
-- Name: clan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clan ALTER COLUMN id SET DEFAULT nextval('public.clan_id_seq'::regclass);


--
-- Name: subscribe id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscribe ALTER COLUMN id SET DEFAULT nextval('public.subscribe_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_detailed_info id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_detailed_info ALTER COLUMN id SET DEFAULT nextval('public.user_detailed_info_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
36c20564359d
\.


--
-- Data for Name: battle_record; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_record (id, subscribe_id, user1_score, user2_score, user1_get_crowns, user2_get_crowns, user1_card_ids, user2_card_ids, replay, "time", winner_id) FROM stdin;
\.


--
-- Data for Name: battle_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.battle_type (id, name) FROM stdin;
\.


--
-- Data for Name: card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.card (id, name, type, level) FROM stdin;
\.


--
-- Data for Name: clan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clan (id, tag, name) FROM stdin;
1	RLPPYLPL	кафедра910
2	RLPPYLPL	кафедра910
3	RLPPYLPL	кафедра910
4	RLPPYLPL	кафедра910
5	RLPPYLPL	кафедра910
6	RLPPYLPL	кафедра910
\.


--
-- Data for Name: subscribe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscribe (id, user_id1, user_id2, battle_type_id) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, password, name, tag, is_super_user, user_detailed_info_id) FROM stdin;
1	admin@mail.ru	$2b$12$EK0Ww/5JDZHe.k6BwTEbDOWSCvgEehXwOOD9xp0U5b8H67nu19N5C	I.Fozzex.I	VGJ80GUR	t	1
2	not_admin@mail.ru	$2b$12$HcZ8bXqSCRgYBTJZsKIIgeXZyw.9knhc4CRwvIsBqDU5v8WeakGO.	I.Fozzex.I	VGJ80GUR	f	2
3	aboba@mail.ru	$2b$12$OZkPBYwi7bqBfwdsWmuHCOXjLdLD6jpmYSzeiGLxhXsq2mlDKmsCm	I.Fozzex.I	VGJ80GUR	f	3
4	123123@mail.ru	$2b$12$e0kFCSwDFpv/kJy/caGq0Oy7IhU7IHhFAGycy1CjWS29cRJA/omfO	I.Fozzex.I	VGJ80GUR	f	4
5	123123123@mail.ru	$2b$12$DFCpn.dtHK/cP40CGc2h4.7NQ1Nh5OWTLNAEfFcdAW5B.FAUitrnO	I.Fozzex.I	VGJ80GUR	f	5
6	VVV@mail.ru	$2b$12$wolPt1t6ZmlF5zyTTqtjWOvHXH5j/kE67LIdz7ph5A01fOJiL8uRe	I.Fozzex.I	VGJ80GUR	f	6
\.


--
-- Data for Name: user_detailed_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_detailed_info (id, crowns, max_crowns, clan_id) FROM stdin;
1	7329	7392	1
2	7329	7392	2
3	7329	7392	3
4	7329	7392	4
5	7329	7392	5
6	7329	7392	6
\.


--
-- Name: battle_record_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.battle_record_id_seq', 1, false);


--
-- Name: battle_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.battle_type_id_seq', 1, false);


--
-- Name: card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.card_id_seq', 1, false);


--
-- Name: clan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clan_id_seq', 6, true);


--
-- Name: subscribe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscribe_id_seq', 1, false);


--
-- Name: user_detailed_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_detailed_info_id_seq', 6, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: battle_record battle_record_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_pkey PRIMARY KEY (id);


--
-- Name: battle_type battle_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_type
    ADD CONSTRAINT battle_type_pkey PRIMARY KEY (id);


--
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- Name: clan clan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clan
    ADD CONSTRAINT clan_pkey PRIMARY KEY (id);


--
-- Name: subscribe subscribe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_pkey PRIMARY KEY (id);


--
-- Name: user_detailed_info user_detailed_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_battle_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_battle_record_id ON public.battle_record USING btree (id);


--
-- Name: ix_battle_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_battle_type_id ON public.battle_type USING btree (id);


--
-- Name: ix_card_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_card_id ON public.card USING btree (id);


--
-- Name: ix_clan_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_clan_id ON public.clan USING btree (id);


--
-- Name: ix_subscribe_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_subscribe_id ON public.subscribe USING btree (id);


--
-- Name: ix_user_detailed_info_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_detailed_info_id ON public.user_detailed_info USING btree (id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: battle_record battle_record_subscribe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_subscribe_id_fkey FOREIGN KEY (subscribe_id) REFERENCES public.subscribe(id) ON DELETE CASCADE;


--
-- Name: battle_record battle_record_winner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES public."user"(id);


--
-- Name: subscribe subscribe_battle_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_battle_type_id_fkey FOREIGN KEY (battle_type_id) REFERENCES public.battle_type(id);


--
-- Name: subscribe subscribe_user_id1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id1_fkey FOREIGN KEY (user_id1) REFERENCES public."user"(id);


--
-- Name: subscribe subscribe_user_id2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id2_fkey FOREIGN KEY (user_id2) REFERENCES public."user"(id);


--
-- Name: user_detailed_info user_detailed_info_clan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clan(id);


--
-- Name: user user_user_detailed_info_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_user_detailed_info_id_fkey FOREIGN KEY (user_detailed_info_id) REFERENCES public.user_detailed_info(id);


--
-- PostgreSQL database dump complete
--

