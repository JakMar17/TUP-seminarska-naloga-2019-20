if exists (select 1
            from  sysobjects
           where  id = object_id('MKB_koda')
            and   type = 'U')
   drop table MKB_koda
go

if exists (select 1
            from  sysobjects
           where  id = object_id('diagnoza')
            and   type = 'U')
   drop table diagnoza
go

if exists (select 1
            from  sysobjects
           where  id = object_id('izvid')
            and   type = 'U')
   drop table izvid
go

if exists (select 1
            from  sysobjects
           where  id = object_id('obravnava')
            and   type = 'U')
   drop table obravnava
go

if exists (select 1
            from  sysobjects
           where  id = object_id('oddelek')
            and   type = 'U')
   drop table oddelek
go

if exists (select 1
            from  sysobjects
           where  id = object_id('pacient')
            and   type = 'U')
   drop table pacient
go

if exists (select 1
            from  sysobjects
           where  id = object_id('preiskava')
            and   type = 'U')
   drop table preiskava
go

/*==============================================================*/
/* Table: MKB_koda                                              */
/*==============================================================*/
create table MKB_koda (
   koda                 varchar(10)          not null,
   si_naziv             varchar(512)         null,
   en_naziv             varchar(512)         null,
   constraint PK_MKB_KODA primary key (koda)
)
go

/*==============================================================*/
/* Table: diagnoza                                              */
/*==============================================================*/
create table diagnoza (
   st_obravnave         int                  not null,
   st_diagnoze          int                  not null,
   ICD_diagnoze         varchar(10)          null,
   koda                 varchar(10)          null,
   constraint PK_DIAGNOZA primary key (st_obravnave, st_diagnoze)
)
go

/*==============================================================*/
/* Table: izvid                                                 */
/*==============================================================*/
create table izvid (
   datum_ura            datetime             null,
   vrednost             float(5)             null,
   id_izvida            int IDENTITY(1,1)    not null,
   ime_preiskave        varchar(100)         not null,
   st_obravnave         int                  not null,
   constraint PK_IZVID primary key (id_izvida)
)
go

/*==============================================================*/
/* Table: obravnava                                             */
/*==============================================================*/
create table obravnava (
   st_obravnave         int                  not null,
   kzz                  int                  not null,
   sifra_oddelka        int                  not null,
   constraint PK_OBRAVNAVA primary key (st_obravnave)
)
go

/*==============================================================*/
/* Table: oddelek                                               */
/*==============================================================*/
create table oddelek (
   sifra_oddelka        int                  not null,
   constraint PK_ODDELEK primary key (sifra_oddelka)
)
go

/*==============================================================*/
/* Table: pacient                                               */
/*==============================================================*/
create table pacient (
   kzz                  int                  not null,
   spol                 char(1)              null,
   starost              int                  null,
   constraint PK_PACIENT primary key (kzz)
)
go

/*==============================================================*/
/* Table: preiskava                                             */
/*==============================================================*/
create table preiskava (
   ime_preiskave        varchar(100)         not null,
   enota                varchar(10)          null,
   sifra_preiskave      int                  null,
   min_rez              float(5)             null,
   max_rez              float(5)             null,
   min_m                float(5)             null,
   max_m                float(5)             null,
   min_z                float(5)             null,
   max_z                float(5)             null,
   constraint PK_PREISKAVA primary key (ime_preiskave)
)
go
