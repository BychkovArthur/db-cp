PGDMP  -    1                |            fastdb    17.2 (Debian 17.2-1.pgdg120+1)    17.2 (Debian 17.2-1.pgdg110+1) G    t           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            u           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            v           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            w           1262    16384    fastdb    DATABASE     q   CREATE DATABASE fastdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE fastdb;
                     postgres    false            �            1259    16385    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16473    battle_record    TABLE     �  CREATE TABLE public.battle_record (
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
       public         heap r       postgres    false            �            1259    16472    battle_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.battle_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.battle_record_id_seq;
       public               postgres    false    231            x           0    0    battle_record_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.battle_record_id_seq OWNED BY public.battle_record.id;
          public               postgres    false    230            �            1259    16391    battle_type    TABLE     U   CREATE TABLE public.battle_type (
    id integer NOT NULL,
    name text NOT NULL
);
    DROP TABLE public.battle_type;
       public         heap r       postgres    false            �            1259    16390    battle_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.battle_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.battle_type_id_seq;
       public               postgres    false    219            y           0    0    battle_type_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.battle_type_id_seq OWNED BY public.battle_type.id;
          public               postgres    false    218            �            1259    16401    card    TABLE     �   CREATE TABLE public.card (
    id integer NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    level integer NOT NULL
);
    DROP TABLE public.card;
       public         heap r       postgres    false            �            1259    16400    card_id_seq    SEQUENCE     �   CREATE SEQUENCE public.card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.card_id_seq;
       public               postgres    false    221            z           0    0    card_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.card_id_seq OWNED BY public.card.id;
          public               postgres    false    220            �            1259    16411    clan    TABLE     e   CREATE TABLE public.clan (
    id integer NOT NULL,
    tag text NOT NULL,
    name text NOT NULL
);
    DROP TABLE public.clan;
       public         heap r       postgres    false            �            1259    16410    clan_id_seq    SEQUENCE     �   CREATE SEQUENCE public.clan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.clan_id_seq;
       public               postgres    false    223            {           0    0    clan_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.clan_id_seq OWNED BY public.clan.id;
          public               postgres    false    222            �            1259    16450 	   subscribe    TABLE     �   CREATE TABLE public.subscribe (
    id integer NOT NULL,
    user_id1 integer NOT NULL,
    user_id2 integer NOT NULL,
    battle_type_id integer NOT NULL
);
    DROP TABLE public.subscribe;
       public         heap r       postgres    false            �            1259    16449    subscribe_id_seq    SEQUENCE     �   CREATE SEQUENCE public.subscribe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.subscribe_id_seq;
       public               postgres    false    229            |           0    0    subscribe_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.subscribe_id_seq OWNED BY public.subscribe.id;
          public               postgres    false    228            �            1259    16434    user    TABLE       CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    tag text NOT NULL,
    is_super_user boolean NOT NULL,
    user_detailed_info_id integer NOT NULL
);
    DROP TABLE public."user";
       public         heap r       postgres    false            �            1259    16421    user_detailed_info    TABLE     �   CREATE TABLE public.user_detailed_info (
    id integer NOT NULL,
    crowns integer NOT NULL,
    max_crowns integer NOT NULL,
    clan_id integer
);
 &   DROP TABLE public.user_detailed_info;
       public         heap r       postgres    false            �            1259    16420    user_detailed_info_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_detailed_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.user_detailed_info_id_seq;
       public               postgres    false    225            }           0    0    user_detailed_info_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.user_detailed_info_id_seq OWNED BY public.user_detailed_info.id;
          public               postgres    false    224            �            1259    16433    user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.user_id_seq;
       public               postgres    false    227            ~           0    0    user_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;
          public               postgres    false    226            �           2604    16476    battle_record id    DEFAULT     t   ALTER TABLE ONLY public.battle_record ALTER COLUMN id SET DEFAULT nextval('public.battle_record_id_seq'::regclass);
 ?   ALTER TABLE public.battle_record ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    231    230    231            �           2604    16394    battle_type id    DEFAULT     p   ALTER TABLE ONLY public.battle_type ALTER COLUMN id SET DEFAULT nextval('public.battle_type_id_seq'::regclass);
 =   ALTER TABLE public.battle_type ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    219    218    219            �           2604    16404    card id    DEFAULT     b   ALTER TABLE ONLY public.card ALTER COLUMN id SET DEFAULT nextval('public.card_id_seq'::regclass);
 6   ALTER TABLE public.card ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    221    221            �           2604    16414    clan id    DEFAULT     b   ALTER TABLE ONLY public.clan ALTER COLUMN id SET DEFAULT nextval('public.clan_id_seq'::regclass);
 6   ALTER TABLE public.clan ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    222    223            �           2604    16453    subscribe id    DEFAULT     l   ALTER TABLE ONLY public.subscribe ALTER COLUMN id SET DEFAULT nextval('public.subscribe_id_seq'::regclass);
 ;   ALTER TABLE public.subscribe ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    229    229            �           2604    16437    user id    DEFAULT     d   ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 8   ALTER TABLE public."user" ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    227    226    227            �           2604    16424    user_detailed_info id    DEFAULT     ~   ALTER TABLE ONLY public.user_detailed_info ALTER COLUMN id SET DEFAULT nextval('public.user_detailed_info_id_seq'::regclass);
 D   ALTER TABLE public.user_detailed_info ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    225    225            c          0    16385    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    217   Q       q          0    16473    battle_record 
   TABLE DATA           �   COPY public.battle_record (id, subscribe_id, user1_score, user2_score, user1_get_crowns, user2_get_crowns, user1_card_ids, user2_card_ids, replay, "time", winner_id) FROM stdin;
    public               postgres    false    231   ;Q       e          0    16391    battle_type 
   TABLE DATA           /   COPY public.battle_type (id, name) FROM stdin;
    public               postgres    false    219   XQ       g          0    16401    card 
   TABLE DATA           5   COPY public.card (id, name, type, level) FROM stdin;
    public               postgres    false    221   uQ       i          0    16411    clan 
   TABLE DATA           -   COPY public.clan (id, tag, name) FROM stdin;
    public               postgres    false    223   �Q       o          0    16450 	   subscribe 
   TABLE DATA           K   COPY public.subscribe (id, user_id1, user_id2, battle_type_id) FROM stdin;
    public               postgres    false    229   �Q       m          0    16434    user 
   TABLE DATA           f   COPY public."user" (id, email, password, name, tag, is_super_user, user_detailed_info_id) FROM stdin;
    public               postgres    false    227   �Q       k          0    16421    user_detailed_info 
   TABLE DATA           M   COPY public.user_detailed_info (id, crowns, max_crowns, clan_id) FROM stdin;
    public               postgres    false    225   �S                  0    0    battle_record_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.battle_record_id_seq', 1, false);
          public               postgres    false    230            �           0    0    battle_type_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.battle_type_id_seq', 1, false);
          public               postgres    false    218            �           0    0    card_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.card_id_seq', 1, false);
          public               postgres    false    220            �           0    0    clan_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.clan_id_seq', 7, true);
          public               postgres    false    222            �           0    0    subscribe_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.subscribe_id_seq', 1, false);
          public               postgres    false    228            �           0    0    user_detailed_info_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.user_detailed_info_id_seq', 7, true);
          public               postgres    false    224            �           0    0    user_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.user_id_seq', 7, true);
          public               postgres    false    226            �           2606    16389 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    217            �           2606    16480     battle_record battle_record_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_pkey;
       public                 postgres    false    231            �           2606    16398    battle_type battle_type_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.battle_type
    ADD CONSTRAINT battle_type_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.battle_type DROP CONSTRAINT battle_type_pkey;
       public                 postgres    false    219            �           2606    16408    card card_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.card DROP CONSTRAINT card_pkey;
       public                 postgres    false    221            �           2606    16418    clan clan_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.clan
    ADD CONSTRAINT clan_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.clan DROP CONSTRAINT clan_pkey;
       public                 postgres    false    223            �           2606    16455    subscribe subscribe_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_pkey;
       public                 postgres    false    229            �           2606    16426 *   user_detailed_info user_detailed_info_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.user_detailed_info DROP CONSTRAINT user_detailed_info_pkey;
       public                 postgres    false    225            �           2606    16441    user user_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public                 postgres    false    227            �           1259    16491    ix_battle_record_id    INDEX     K   CREATE INDEX ix_battle_record_id ON public.battle_record USING btree (id);
 '   DROP INDEX public.ix_battle_record_id;
       public                 postgres    false    231            �           1259    16399    ix_battle_type_id    INDEX     G   CREATE INDEX ix_battle_type_id ON public.battle_type USING btree (id);
 %   DROP INDEX public.ix_battle_type_id;
       public                 postgres    false    219            �           1259    16409 
   ix_card_id    INDEX     9   CREATE INDEX ix_card_id ON public.card USING btree (id);
    DROP INDEX public.ix_card_id;
       public                 postgres    false    221            �           1259    16419 
   ix_clan_id    INDEX     9   CREATE INDEX ix_clan_id ON public.clan USING btree (id);
    DROP INDEX public.ix_clan_id;
       public                 postgres    false    223            �           1259    16471    ix_subscribe_id    INDEX     C   CREATE INDEX ix_subscribe_id ON public.subscribe USING btree (id);
 #   DROP INDEX public.ix_subscribe_id;
       public                 postgres    false    229            �           1259    16432    ix_user_detailed_info_id    INDEX     U   CREATE INDEX ix_user_detailed_info_id ON public.user_detailed_info USING btree (id);
 ,   DROP INDEX public.ix_user_detailed_info_id;
       public                 postgres    false    225            �           1259    16447    ix_user_email    INDEX     H   CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);
 !   DROP INDEX public.ix_user_email;
       public                 postgres    false    227            �           1259    16448 
   ix_user_id    INDEX     ;   CREATE INDEX ix_user_id ON public."user" USING btree (id);
    DROP INDEX public.ix_user_id;
       public                 postgres    false    227            �           2606    16481 -   battle_record battle_record_subscribe_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_subscribe_id_fkey FOREIGN KEY (subscribe_id) REFERENCES public.subscribe(id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_subscribe_id_fkey;
       public               postgres    false    231    229    3271            �           2606    16486 *   battle_record battle_record_winner_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.battle_record
    ADD CONSTRAINT battle_record_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES public."user"(id);
 T   ALTER TABLE ONLY public.battle_record DROP CONSTRAINT battle_record_winner_id_fkey;
       public               postgres    false    3268    227    231            �           2606    16456 '   subscribe subscribe_battle_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_battle_type_id_fkey FOREIGN KEY (battle_type_id) REFERENCES public.battle_type(id);
 Q   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_battle_type_id_fkey;
       public               postgres    false    219    229    3254            �           2606    16461 !   subscribe subscribe_user_id1_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id1_fkey FOREIGN KEY (user_id1) REFERENCES public."user"(id);
 K   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_user_id1_fkey;
       public               postgres    false    229    3268    227            �           2606    16466 !   subscribe subscribe_user_id2_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.subscribe
    ADD CONSTRAINT subscribe_user_id2_fkey FOREIGN KEY (user_id2) REFERENCES public."user"(id);
 K   ALTER TABLE ONLY public.subscribe DROP CONSTRAINT subscribe_user_id2_fkey;
       public               postgres    false    227    229    3268            �           2606    16427 2   user_detailed_info user_detailed_info_clan_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_detailed_info
    ADD CONSTRAINT user_detailed_info_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clan(id);
 \   ALTER TABLE ONLY public.user_detailed_info DROP CONSTRAINT user_detailed_info_clan_id_fkey;
       public               postgres    false    223    225    3260            �           2606    16442 $   user user_user_detailed_info_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_user_detailed_info_id_fkey FOREIGN KEY (user_detailed_info_id) REFERENCES public.user_detailed_info(id);
 P   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_user_detailed_info_id_fkey;
       public               postgres    false    227    3264    225            c      x�36K6205316�L����� %��      q      x������ � �      e      x������ � �      g      x������ � �      i   >   x�3��	��	�ἰ��-�^�r���KC.#|���$M�I��4�'i�O2F��� jU`      o      x������ � �      m   �  x�u�ɮ�@ @�u���A��]3KAI'&-@��w'�V>M���� J���UE�~��L�g�0�֜?��VC3��(�{-V��)�E�h0��w@��q}�W� ��3{@{��gP��?o!3	�q�z�{9�{;�֖uɂp᪬i�P�q�:�UhX�YT���@`� �oq􊐰�ʧ1�q+�Ǵ󫻩��pRG��:y�,7��V�����2g���zU2��oT�f`K{b��h92a��eR]2�d����U��{��䃲`з�Ru��aڛk6�.8�H��x��7�l$��'��#��!��ObDp<_��v��|/��UG�i�o��'���`KMĎ�>qC���gb����f���_�;�4Q��.�ک�w)i�{fx���ΙL��ym$���q=�����xH��      k   4   x�MǱ  ��	�$b��J7'�:����M�-ضMڒ�mk�S*     