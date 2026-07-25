-- 통합 테스트용 소형 U9C-유사 스키마 (idempotent)
IF OBJECT_ID('dbo.PM_Receivement', 'U') IS NOT NULL DROP TABLE dbo.PM_Receivement;
IF OBJECT_ID('dbo.CBO_ItemMaster_Trl', 'U') IS NOT NULL DROP TABLE dbo.CBO_ItemMaster_Trl;
GO
CREATE TABLE dbo.PM_Receivement (
    ID bigint NOT NULL PRIMARY KEY,
    Org bigint NOT NULL,
    DocNo nvarchar(40) NOT NULL,
    CreatedOn datetime NULL,
    SysMlFlag int NULL
);
GO
CREATE TABLE dbo.CBO_ItemMaster_Trl (
    ID bigint NOT NULL PRIMARY KEY,
    Name nvarchar(200) NULL
);
GO
INSERT INTO dbo.PM_Receivement (ID, Org, DocNo) VALUES (1, 100, 'RCV-0001');
INSERT INTO dbo.CBO_ItemMaster_Trl (ID, Name) VALUES (1, N'품목A');
GO
