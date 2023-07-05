--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: likes; Type: TABLE; Schema: public; Owner: artemkhmelev
--

CREATE TABLE public.likes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    post_id integer NOT NULL,
    is_like boolean
);


ALTER TABLE public.likes OWNER TO artemkhmelev;

--
-- Name: likes_id_seq; Type: SEQUENCE; Schema: public; Owner: artemkhmelev
--

CREATE SEQUENCE public.likes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.likes_id_seq OWNER TO artemkhmelev;

--
-- Name: likes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: artemkhmelev
--

ALTER SEQUENCE public.likes_id_seq OWNED BY public.likes.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: artemkhmelev
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    user_id integer
);


ALTER TABLE public.posts OWNER TO artemkhmelev;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: artemkhmelev
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO artemkhmelev;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: artemkhmelev
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: artemkhmelev
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    age character varying(255)
);


ALTER TABLE public.users OWNER TO artemkhmelev;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: artemkhmelev
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO artemkhmelev;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: artemkhmelev
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: likes id; Type: DEFAULT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.likes ALTER COLUMN id SET DEFAULT nextval('public.likes_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: artemkhmelev
--

COPY public.likes (id, user_id, post_id, is_like) FROM stdin;
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: artemkhmelev
--

COPY public.posts (id, title, content, user_id) FROM stdin;
19	333	444	6
21	qqq	aaa	6
22	vvv	bbb	6
23	123q    qq	222fff	6
24	666ffff	ggg222	6
25	666ffff	ggg222	6
26	666ffff	ggg222	6
27	666ffff	ggg222	8
20			6
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: artemkhmelev
--

COPY public.users (id, username, password, first_name, last_name, age) FROM stdin;
6	test1	1b4f0e9851971998e732078544c96b36c3d01cedf7caa332359d6f1d83567014	\N	\N	\N
7	test2	60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752	\N	\N	\N
8	test3	fd61a03af4f77d870fc21e05e7e80678095c92d808cfb3b5c279ee04c74aca13	\N	\N	\N
\.


--
-- Name: likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: artemkhmelev
--

SELECT pg_catalog.setval('public.likes_id_seq', 4, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: artemkhmelev
--

SELECT pg_catalog.setval('public.posts_id_seq', 29, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: artemkhmelev
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: likes likes_pkey; Type: CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: likes likes_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: likes likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: artemkhmelev
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

