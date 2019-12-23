drop index MKB_koda_PK;

drop table MKB_koda;


drop index diagnoza_obravnava_FK;

drop index diagnoza_PK;

drop table diagnoza;

drop index izvid_preiskava_FK;

drop index izvid_obravnava_FK;

drop index izvid_PK;

drop table izvid;

drop index oddelek_obravnava_FK;

drop index pacient_obravnava_FK;

drop index obravnava_PK;

drop table obravnava;

drop index oddelek_PK;

drop table oddelek;

drop index pacient_PK;

drop table pacient;

drop index preiskava_PK;

drop table preiskava;

/*==============================================================*/
/* Table: MKB_koda                                              */
/*==============================================================*/
create table MKB_koda (
   koda                 VARCHAR(10)          not null,
   si_naziv             VARCHAR(512)         null,
   en_naziv             VARCHAR(512)         null,
   constraint PK_MKB_KODA primary key (koda)
);

/*==============================================================*/
/* Index: MKB_koda_PK                                           */
/*==============================================================*/
create unique index MKB_koda_PK on MKB_koda (
koda
);

/*==============================================================*/
/* Table: diagnoza                                              */
/*==============================================================*/
create table diagnoza (
   st_obravnave         INT4                 not null,
   st_diagnoze          INT4                 not null,
   ICD_diagnoze         VARCHAR(10)          null,
   constraint PK_DIAGNOZA primary key (st_obravnave, st_diagnoze)
);

/*==============================================================*/
/* Index: diagnoza_PK                                           */
/*==============================================================*/
create unique index diagnoza_PK on diagnoza (
st_obravnave,
st_diagnoze
);

/*==============================================================*/
/* Index: diagnoza_obravnava_FK                                 */
/*==============================================================*/
create  index diagnoza_obravnava_FK on diagnoza (
st_obravnave
);

/*==============================================================*/
/* Table: izvid                                                 */
/*==============================================================*/
create table izvid (
   datum_ura            DATE                 null,
   vrednost             float(5)               null,
   id_izvida            Serial                 not null,
   ime_preiskave        VARCHAR(100)         not null,
   st_obravnave         INT4                 not null,
   constraint PK_IZVID primary key (id_izvida)
);

/*==============================================================*/
/* Index: izvid_PK                                              */
/*==============================================================*/
create unique index izvid_PK on izvid (
id_izvida
);

/*==============================================================*/
/* Index: izvid_obravnava_FK                                    */
/*==============================================================*/
create  index izvid_obravnava_FK on izvid (
st_obravnave
);

/*==============================================================*/
/* Index: izvid_preiskava_FK                                    */
/*==============================================================*/
create  index izvid_preiskava_FK on izvid (
ime_preiskave
);

/*==============================================================*/
/* Table: obravnava                                             */
/*==============================================================*/
create table obravnava (
   st_obravnave         INT4                 not null,
   kzz                  INT4                 not null,
   sifra_oddelka        INT4                 not null,
   constraint PK_OBRAVNAVA primary key (st_obravnave)
);

/*==============================================================*/
/* Index: obravnava_PK                                          */
/*==============================================================*/
create unique index obravnava_PK on obravnava (
st_obravnave
);

/*==============================================================*/
/* Index: pacient_obravnava_FK                                  */
/*==============================================================*/
create  index pacient_obravnava_FK on obravnava (
kzz
);

/*==============================================================*/
/* Index: oddelek_obravnava_FK                                  */
/*==============================================================*/
create  index oddelek_obravnava_FK on obravnava (
sifra_oddelka
);

/*==============================================================*/
/* Table: oddelek                                               */
/*==============================================================*/
create table oddelek (
   sifra_oddelka        INT4                 not null,
   constraint PK_ODDELEK primary key (sifra_oddelka)
);

/*==============================================================*/
/* Index: oddelek_PK                                            */
/*==============================================================*/
create unique index oddelek_PK on oddelek (
sifra_oddelka
);

/*==============================================================*/
/* Table: pacient                                               */
/*==============================================================*/
create table pacient (
   kzz                  INT4                 not null,
   spol                 CHAR(1)              null,
   starost              INT4                 null,
   constraint PK_PACIENT primary key (kzz)
);

/*==============================================================*/
/* Index: pacient_PK                                            */
/*==============================================================*/
create unique index pacient_PK on pacient (
kzz
);

/*==============================================================*/
/* Table: preiskava                                             */
/*==============================================================*/
create table preiskava (
   ime_preiskave        VARCHAR(100)         not null,
   enota                VARCHAR(10)          null,
   sifra_preiskave      INT4                 null,
   min_rez              float(5)               null,
   max_rez              float(5)               null,
   min_m                float(5)               null,
   max_m                float(5)               null,
   min_z                float(5)               null,
   max_z                float(5)               null,
   constraint PK_PREISKAVA primary key (ime_preiskave)
);

/*==============================================================*/
/* Index: preiskava_PK                                          */
/*==============================================================*/
create unique index preiskava_PK on preiskava (
ime_preiskave
);
