PGDMP  !                    |            fastdb    17.2 (Debian 17.2-1.pgdg120+1)    17.2 (Debian 17.2-1.pgdg110+1) @    o           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            p           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            q           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            r           1262    16384    fastdb    DATABASE     q   CREATE DATABASE fastdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE fastdb;
                     postgres    false            �            1259    16482    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16455    battle_record    TABLE     �  CREATE TABLE public.battle_record (
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
 !   DROP TABLE public.battle_record;
       public         heap r       postgres    false            �            1259    16454    battle_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.battle_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.battle_record_id_seq;
       public               postgres    false    228            s           0    0    battle_record_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.battle_record_id_seq OWNED BY public.battle_record.id;
          public               postgres    false    227            �            1259    16407    battle_type    TABLE     U   CREATE TABLE public.battle_type (
    id integer NOT NULL,
    name text NOT NULL
);
    DROP TABLE public.battle_type;
       public         heap r       postgres    false            �            1259    16406    battle_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.battle_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.battle_type_id_seq;
       public               postgres    false    222            t           0    0    battle_type_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.battle_type_id_seq OWNED BY public.battle_type.id;
          public               postgres    false    221            �            1259    16474    card    TABLE     �   CREATE TABLE public.card (
    id integer NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    level integer NOT NULL
);
    DROP TABLE public.card;
       public         heap r       postgres    false            �            1259    16473    card_id_seq    SEQUENCE     �   CREATE SEQUENCE public.card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.card_id_seq;
       public               postgres    false    230            u           0    0    card_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.card_id_seq OWNED BY public.card.id;
          public               postgres    false    229            �            1259    16386    clan    TABLE     e   CREATE TABLE public.clan (
    id integer NOT NULL,
    tag text NOT NULL,
    name text NOT NULL
);
    DROP TABLE public.clan;
       public         heap r       postgres    false            �            1259    16385    clan_id_seq    SEQUENCE     �   CREATE SEQUENCE public.clan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.clan_id_seq;
       public               postgres    false    218            v           0    0    clan_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.clan_id_seq OWNED BY public.clan.id;
          public               postgres    false    217            �            1259    16433 	   subscribe    TABLE     �   CREATE TABLE public.subscribe (
    id integer NOT NULL,
    user_id1 integer NOT NULL,
    user_id2 integer NOT NULL,
    battle_type_id integer NOT NULL
);
    DROP TABLE public.subscribe;
       public         heap r       postgres    false            �            1259    16432    subscribe_id_seq    SEQUENCE     �   CREATE SEQUENCE public.subscribe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.subscribe_id_seq;
       public               postgres    false    226            w           0    0    subscribe_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.subscribe_id_seq OWNED BY public.subscribe.id;
          public               postgres    false    225            �            1259    16416    user    TABLE       CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password text NOT NULL,
    name character varying(100),
    tag text NOT NULL,
    is_super_user boolean DEFAULT false NOT NULL,
    user_detailed_info_id integer
);
    DROP TABLE public."user";
       public         heap r       postgres    false            �            1259    16395    user_detailed_info    TABLE     �   CREATE TABLE public.user_detailed_info (
    id integer NOT NULL,
    crowns integer NOT NULL,
    max_crowns integer NOT NULL,
    clan_id integer,
    updated_ts timestamp without time zone
);
 &   DROP TABLE public.user_detailed_info;
       public         heap r       postgres    false            �            1259    16394    user_detailed_info_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_detailed_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.user_detailed_info_id_seq;
       public               postgres    false    220            x           0    0    user_detailed_info_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.user_detailed_info_id_seq OWNED BY public.user_detailed_info.id;
          public               postgres    false    219            �            1259    16415    user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.user_id_seq;
       public               postgres    false    224            y           0    0    user_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;
          public               postgres    false    223            �           2604    16458    battle_record id    DEFAULT     t   ALTER TABLE ONLY public.battle_record ALTER COLUMN id SET DEFAULT nextval('public.battle_record_id_seq'::regclass);
 ?   ALTER TABLE public.battle_record ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    16410    battle_type id    DEFAULT     p   ALTER TABLE ONLY public.battle_type ALTER COLUMN id SET DEFAULT nextval('public.battle_type_id_seq'::regclass);
 =   ALTER TABLE public.battle_type ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    221    222    222            �           2604    16477    card id    DEFAULT     b   ALTER TABLE ONLY public.card ALTER COLUMN id SET DEFAULT nextval('public.card_id_seq'::regclass);
 6   ALTER TABLE public.card ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    230    229    230            �           2604    16389    clan id    DEFAULT     b   ALTER TABLE ONLY public.clan ALTER COLUMN id SET DEFAULT nextval('public.clan_id_seq'::regclass);
 6   ALTER TABLE public.clan ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    16436    subscribe id    DEFAULT     l   ALTER TABLE ONLY public.subscribe ALTER COLUMN id SET DEFAULT nextval('public.subscribe_id_seq'::regclass);
 ;   ALTER TABLE public.subscribe ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225    226            �           2604    16419    user id    DEFAULT     d   ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 8   ALTER TABLE public."user" ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223    224            �           2604    16398    user_detailed_info id    DEFAULT     ~   ALTER TABLE ONLY public.user_detailed_info ALTER COLUMN id SET DEFAULT nextval('public.user_detailed_info_id_seq'::regclass);
 D   ALTER TABLE public.user_detailed_info ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219    220            l          0    16482    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    231   �J       i          0    16455    battle_record 
   TABLE DATA           �   COPY public.battle_record (id, subscribe_id, user1_score, user2_score, user1_get_crowns, user2_get_crowns, user1_card_ids, user2_card_ids, replay, "time", winner_id) FROM stdin;
    public               postgres    false    228   �J       c          0    16407    battle_type 
   TABLE DATA           /   COPY public.battle_type (id, name) FROM stdin;
    public               postgres    false    222    K       k          0    16474    card 
   TABLE DATA           5   COPY public.card (id, name, type, level) FROM stdin;
    public               postgres    false    230   0K       _          0    16386    clan 
   TABLE DATA           -   COPY public.clan (id, tag, name) FROM stdin;
    public               postgres    false    218   �K       g          0    16433 	   subscribe 
   TABLE DATA           K   COPY public.subscribe (id, user_id1, user_id2, battle_type_id) FROM stdin;
    public               postgres    false    226   �K       e          0    16416    user 
   TABLE DATA           f   COPY public."user" (id, email, password, name, tag, is_super_user, user_detailed_info_id) FROM stdin;
    public               postgres    false    224   L       a          0    16395    user_detailed_info 
   TABLE DATA           Y   COPY public.user_detailed_info (id, crowns, max_crowns, clan_id, updated_ts) FROM stdin;
    public               postgres    false    220   �L       z           0    0    battle_record_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.battle_record_id_seq', 6, true);
          public               postgres    false    227            {           0    0    battle_type_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.battle_type_id_seq', 2, true);
          public               postgres    false    221            |           0    0    card_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.card_id_seq', 4, true);
          public               postgres    false    229            }           0    0    clan_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.clan_id_seq', 3, true);
          public               postgres    false    217            ~           0    0    subscribe_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.subscribe_id_seq', 8, true);
          public               postgres    false    225                       0    0    user_detailed_info_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.user_detailed_info_id_seq', 4, true);
          public               postgres    false    219            �           0    0    user_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.user_id_seq', 4, true);
          public               postgres    false    223            �           2606    16486 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    231            �           2606    16462     battle_record battle_record_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_pkey;
       public                 postgres    false    228            �           2606    16414    battle_type battle_type_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.battle_type
    ADD CONSTRAINT battle_type_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.battle_type DROP CONSTRAINT battle_type_pkey;
       public                 postgres    false    222            �           2606    16481    card card_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.card DROP CONSTRAINT card_pkey;
       public                 postgres    false    230            �           2606    16393    clan clan_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.clan
    ADD CONSTRAINT clan_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.clan DROP CONSTRAINT clan_pkey;
       public                 postgres    false    218            �           2606    16438    subscribe subscribe_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_pkey;
       public                 postgres    false    226            �           2606    16400 *   user_detailed_info user_detailed_info_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.user_detailed_info DROP CONSTRAINT user_detailed_info_pkey;
       public                 postgres    false    220            �           2606    16426    user user_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_email_key;
       public                 postgres    false    224            �           2606    16424    user user_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public                 postgres    false    224            �           2606    16463 -   battle_record battle_record_subscribe_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_subscribe_id_fkey FOREIGN KEY (subscribe_id) REFERENCES public.subscribe(id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_subscribe_id_fkey;
       public               postgres    false    3263    226    228            �           2606    16468 *   battle_record battle_record_winner_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES public."user"(id);
 T   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_winner_id_fkey;
       public               postgres    false    224    228    3261            �           2606    16449 '   subscribe subscribe_battle_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_battle_type_id_fkey FOREIGN KEY (battle_type_id) REFERENCES public.battle_type(id);
 Q   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_battle_type_id_fkey;
       public               postgres    false    3257    222    226            �           2606    16439 !   subscribe subscribe_user_id1_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id1_fkey FOREIGN KEY (user_id1) REFERENCES public."user"(id);
 K   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_user_id1_fkey;
       public               postgres    false    3261    226    224            �           2606    16444 !   subscribe subscribe_user_id2_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id2_fkey FOREIGN KEY (user_id2) REFERENCES public."user"(id);
 K   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_user_id2_fkey;
       public               postgres    false    3261    226    224            �           2606    16401 2   user_detailed_info user_detailed_info_clan_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clan(id);
 \   ALTER TABLE ONLY public.user_detailed_info DROP CONSTRAINT user_detailed_info_clan_id_fkey;
       public               postgres    false    220    3253    218            �           2606    16427 $   user user_user_detailed_info_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_user_detailed_info_id_fkey FOREIGN KEY (user_detailed_info_id) REFERENCES public.user_detailed_info(id);
 P   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_user_detailed_info_id_fkey;
       public               postgres    false    220    224    3255            l      x������ � �      i   N   x�����0����D9�*�� �Dٽ�З����(6��vh��zaâ��ȋ6���̌�@	D`������|(\%      c       x�3�J,��K�2�tIMK,�)����� U�\      k   D   x�3�t��I���,HUp�4�2�(��KN-.��9qqs�f��s�p�$U�T�p��qqq 1M      _   9   x�3�,IL�5�0��-�^�r���KC.#����!�1X�Sʈ+F��� ��&�      g   *   x�3�4�4�4�2�&@ڌ�(b�e�A�@$���� |&[      e   �   x�����0����S�`��ҝ���ʠƍ�*�2Ex|	���?��0t��ne��.A!�������_��{	���6}��.ˎ������3�ҡ�3�kUu��Mg�[�JBꇶ�'���:����DJi$�@�>u}n�h�>J�������i2f��u�I��S�#d����!}      a   -   x�3�4426�453��4���2B0	#	�Lе��qqq �j*     