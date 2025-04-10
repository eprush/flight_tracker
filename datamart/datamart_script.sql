CREATE VIEW counting_datamart AS
    SELECT DISTINCT COUNT(*) AS count, aircraft, airline FROM flightdata
    GROUP BY aircraft, airline;

SELECT * FROM counting_datamart;