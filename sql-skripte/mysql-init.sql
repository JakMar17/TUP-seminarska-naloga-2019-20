drop table if exists MKB_koda;

drop table if exists diagnoza;

drop table if exists izvid;

drop table if exists obravnava;

drop table if exists oddelek;

drop table if exists pacient;

drop table if exists preiskava;

/*==============================================================*/
/* Table: MKB_koda                                              */
/*==============================================================*/
create table MKB_koda
(
   koda                 varchar(10) not null,
   si_naziv             varchar(512),
   en_naziv             varchar(512),
   primary key (koda)
);

/*==============================================================*/
/* Table: diagnoza                                              */
/*==============================================================*/
create table diagnoza
(
   st_obravnave         int not null,
   st_diagnoze          int not null,
   ICD_diagnoze         varchar(10),
   koda                 varchar(10),
   primary key (st_obravnave, st_diagnoze)
);

/*==============================================================*/
/* Table: izvid                                                 */
/*==============================================================*/
create table izvid
(
   datum_ura            datetime,
   vrednost             float(5),
   id_izvida            int not null AUTO_INCREMENT,
   ime_preiskave        varchar(100) not null,
   st_obravnave         int not null,
   primary key (id_izvida)
);

/*==============================================================*/
/* Table: obravnava                                             */
/*==============================================================*/
create table obravnava
(
   st_obravnave         int not null,
   kzz                  int not null,
   sifra_oddelka        int not null,
   primary key (st_obravnave)
);

/*==============================================================*/
/* Table: oddelek                                               */
/*==============================================================*/
create table oddelek
(
   sifra_oddelka        int not null,
   primary key (sifra_oddelka)
);

/*==============================================================*/
/* Table: pacient                                               */
/*==============================================================*/
create table pacient
(
   kzz                  int not null,
   spol                 char(1),
   starost              int,
   primary key (kzz)
);

/*==============================================================*/
/* Table: preiskava                                             */
/*==============================================================*/
create table preiskava
(
   ime_preiskave        varchar(100) not null,
   enota                varchar(10),
   sifra_preiskave      int,
   min_rez              float(5),
   max_rez              float(5),
   min_m                float(5),
   max_m                float(5),
   min_z                float(5),
   max_z                float(5),
   primary key (ime_preiskave)
);

