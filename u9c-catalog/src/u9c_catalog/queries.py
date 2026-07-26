# 시스템 카탈로그에서 스키마 메타데이터를 뽑는 T-SQL 쿼리 모음
TABLES_AND_VIEWS = """
SELECT s.name AS [schema], o.name AS [name],
       CASE o.type WHEN 'U' THEN 'TABLE' ELSE 'VIEW' END AS object_type
FROM sys.objects o
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE o.type IN ('U','V')
ORDER BY s.name, o.name;
"""

COLUMNS = """
SELECT s.name AS [schema], o.name AS [table],
       c.name AS [column], t.name AS data_type,
       c.max_length AS max_length,
       c.precision AS [precision], c.scale AS [scale],
       c.is_nullable AS is_nullable,
       c.is_identity AS is_identity, c.column_id AS ordinal,
       CAST(CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS bit) AS is_pk,
       dc.definition AS default_definition
FROM sys.columns c
JOIN sys.objects o ON o.object_id = c.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
JOIN sys.types t ON t.user_type_id = c.user_type_id
LEFT JOIN sys.default_constraints dc ON dc.object_id = c.default_object_id
LEFT JOIN (
    SELECT ic.object_id, ic.column_id
    FROM sys.indexes i
    JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
    WHERE i.is_primary_key = 1
) pk ON pk.object_id = c.object_id AND pk.column_id = c.column_id
WHERE o.type IN ('U','V')
ORDER BY s.name, o.name, c.column_id;
"""

ROUTINES = """
SELECT s.name AS [schema], o.name AS [name],
       CASE o.type WHEN 'P' THEN 'PROCEDURE' ELSE 'FUNCTION' END AS object_type,
       m.definition AS definition
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE o.type IN ('P','FN','IF','TF')
ORDER BY s.name, o.name;
"""

FOREIGN_KEYS = """
SELECT sp.name + '.' + tp.name AS from_object,
       sr.name + '.' + tr.name AS to_object,
       fk.name AS detail
FROM sys.foreign_keys fk
JOIN sys.tables tp ON tp.object_id = fk.parent_object_id
JOIN sys.schemas sp ON sp.schema_id = tp.schema_id
JOIN sys.tables tr ON tr.object_id = fk.referenced_object_id
JOIN sys.schemas sr ON sr.schema_id = tr.schema_id;
"""

ROW_COUNTS = """
SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name;
"""
