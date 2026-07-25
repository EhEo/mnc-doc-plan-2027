-- ERP_Catalog: U9C 메타데이터 스냅샷 저장 스키마 (idempotent 생성)
IF SCHEMA_ID('catalog') IS NULL EXEC('CREATE SCHEMA catalog');
GO
IF OBJECT_ID('catalog.snapshots','U') IS NULL
CREATE TABLE catalog.snapshots (
    snapshot_id   int IDENTITY(1,1) PRIMARY KEY,
    label         nvarchar(100) NOT NULL,
    created_on    datetime2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
IF OBJECT_ID('catalog.objects','U') IS NULL
CREATE TABLE catalog.objects (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    object_type   nvarchar(20) NOT NULL,
    row_count     bigint NULL,
    is_auxiliary  bit NOT NULL DEFAULT 0,
    aux_reason    nvarchar(200) NULL,
    CONSTRAINT PK_catalog_objects PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.columns','U') IS NULL
CREATE TABLE catalog.columns (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    column_name   nvarchar(128) NOT NULL,
    data_type     nvarchar(64) NOT NULL,
    is_nullable   bit NOT NULL,
    is_pk         bit NOT NULL,
    is_system     bit NOT NULL DEFAULT 0,
    system_reason nvarchar(200) NULL,
    ordinal       int NOT NULL,
    CONSTRAINT PK_catalog_columns PRIMARY KEY (snapshot_id, schema_name, object_name, column_name)
);
GO
IF OBJECT_ID('catalog.dependencies','U') IS NULL
CREATE TABLE catalog.dependencies (
    snapshot_id   int NOT NULL,
    from_object   nvarchar(384) NOT NULL,
    to_object     nvarchar(384) NOT NULL,
    kind          nvarchar(20) NOT NULL,
    detail        nvarchar(256) NULL
);
GO
IF OBJECT_ID('catalog.routines','U') IS NULL
CREATE TABLE catalog.routines (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    object_type   nvarchar(20) NOT NULL,
    definition    nvarchar(max) NULL,
    CONSTRAINT PK_catalog_routines PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
