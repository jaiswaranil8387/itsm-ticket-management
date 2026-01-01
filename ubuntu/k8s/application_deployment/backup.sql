--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg110+1)
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
-- Name: tickets; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.tickets (
    id bigint NOT NULL,
    title text,
    description text,
    priority text,
    status text,
    created_at text
);


ALTER TABLE public.tickets OWNER TO app;

--
-- Name: tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE public.tickets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tickets_id_seq OWNER TO app;

--
-- Name: tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE public.tickets_id_seq OWNED BY public.tickets.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username text,
    password text,
    role text
);


ALTER TABLE public.users OWNER TO app;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO app;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: tickets id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.tickets ALTER COLUMN id SET DEFAULT nextval('public.tickets_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.tickets (id, title, description, priority, status, created_at) FROM stdin;
3	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
4	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
5	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
6	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
7	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
8	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
9	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
10	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
11	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
12	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
13	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
14	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
15	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
16	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
17	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
18	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
19	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
20	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
21	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
22	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
23	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
24	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
25	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
26	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
27	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
28	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
29	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
30	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
31	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
32	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
33	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
34	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
35	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
36	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
37	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
38	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
39	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
40	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
41	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
42	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
43	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
44	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
45	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
46	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
47	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
48	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
49	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
50	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
51	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
52	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
53	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
54	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
55	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
56	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
57	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
58	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
59	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
60	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
61	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
62	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
63	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
64	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
65	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
66	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
67	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
2	Application Crash	App crashes during data import	Low	Open	2025-07-20 11:15:00
68	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
69	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
70	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
71	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
72	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
73	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
74	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
75	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
76	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
77	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
78	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
79	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
80	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
81	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
82	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
83	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
84	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
85	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
86	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
87	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
88	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
89	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
90	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
91	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
92	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
93	Login Failure	User reports login issue on portal	High	Open	2025-07-20 10:00:00
94	Application Crash	App crashes during data import	High	In Progress	2025-07-20 11:15:00
95	Report Generation Issue	Report not generating correctly	Medium	Open	2025-07-20 12:30:00
96	UI Glitch	Minor display issue on dashboard	Low	Resolved	2025-07-20 09:45:00
97	login failed	failed during login	High	Resolved	2025-07-25 13:15:16
98	test	test	High	Open	2025-07-25 15:02:54
99	Report Generation Issue	issue while Report Generation 	High	Open	2025-08-01 17:31:17
100	application Crash	application crash while running at 12	High	In Progress	2025-08-02 02:40:44
101	login failed	login failed,updated	Medium	Open	2025-08-02 03:50:25
102	testq	testtq	High	Open	2025-08-02 17:31:19
103	testm	testm	Medium	Open	2025-08-02 17:32:46
1	Login Failure	User reports login issue on portals, updated	Medium	Open	2025-07-20 10:00:00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.users (id, username, password, role) FROM stdin;
1	admin	scrypt:32768:8:1$ahZoAsUNfo3Ck1Mk$d7335b843abba67d745b764cdc2b422671d49fc8917a08cd30ed1f8ef6a4adea07b01c9d1ce374fd7d583da235bbefeb63996fe56df999d4da3e7f9a679ab743	admin
2	test	scrypt:32768:8:1$ZuNip9gM9hyA7C6z$f327e3ec88da884c984266873650221cd87570582167aeba7ede2bddcb2168e53aa60ce2bde6fd2f4c895272a3e3f2eb1040ee7bc7919938591534bade5fae2b	readonly
4	test2	scrypt:32768:8:1$RUUHs3zCr9IgDWJj$e2a8296e4be9622c6384cc903df349c9e27aaa634f2f2368c94f36e94393b8ce734157693e63edde109ec1f12d1881a3e3068578f4b214dda9ec069abe32c5a4	admin
5	test3	scrypt:32768:8:1$C3BOkyobl4eRuRhM$cc071eb8ebeb18b16160f2a35eb7a37fefe704417c1872502b642438f0902653d6ede91bc37db38718e8cf84ecab295cc8105180be52c9254d59385be899b320	readonly
14	test4	scrypt:32768:8:1$WCEdaSI5RLJtDcYu$632330e92161f2086ffc61272265415bf80fc478772213d5057e3002ee9e2581c50e4322e3222a011dd9bb3e485e45c2fae885f333a4914ce0f5e4a975b9443b	admin
\.


--
-- Name: tickets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('public.tickets_id_seq', 103, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('public.users_id_seq', 14, true);


--
-- Name: tickets idx_16392_tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT idx_16392_tickets_pkey PRIMARY KEY (id);


--
-- Name: users idx_16399_users_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT idx_16399_users_pkey PRIMARY KEY (id);


--
-- Name: idx_16399_sqlite_autoindex_users_1; Type: INDEX; Schema: public; Owner: app
--

CREATE UNIQUE INDEX idx_16399_sqlite_autoindex_users_1 ON public.users USING btree (username);


--
-- PostgreSQL database dump complete
--

