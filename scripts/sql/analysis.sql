--Basic KPI

SELECT
    COUNT(*) AS total_tickets,

    ROUND(AVG(resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(csat), 2)
        AS avg_csat,

    ROUND(AVG(quality_score), 2)
        AS avg_quality_score,

    ROUND(AVG(CAST(sla_met AS FLOAT)) * 100, 2)
        AS sla_compliance_pct,

    ROUND(AVG(CAST(fcr AS FLOAT)) * 100, 2)
        AS fcr_rate_pct,

    ROUND(AVG(CAST(reopened AS FLOAT)) * 100, 2)
        AS reopen_rate_pct

FROM support_tickets;

-- Comparing teams

SELECT
    team,
    COUNT(*) AS total_tickets,

    ROUND(AVG(resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(csat), 2)
        AS avg_csat,

    ROUND(AVG(quality_score), 2)
        AS avg_quality,

    ROUND(AVG(CAST(sla_met AS FLOAT)) * 100, 2)
        AS sla_compliance,

    ROUND(AVG(CAST(fcr AS FLOAT)) * 100, 2)
        AS fcr_rate

FROM support_tickets

GROUP BY team

ORDER BY avg_resolution_time DESC;

-- Analyzing the agents


SELECT
    t.agent_id,
    a.team,
    a.experience_months,
    a.shift,

    COUNT(*) AS tickets_handled,

    ROUND(AVG(t.resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(t.csat), 2)
        AS avg_csat,

    ROUND(AVG(t.quality_score), 2)
        AS avg_quality,

    ROUND(AVG(CAST(t.fcr AS FLOAT)) * 100, 2)
        AS fcr_rate

FROM support_tickets t

JOIN agents a
    ON t.agent_id = a.agent_id

GROUP BY
    t.agent_id,
    a.team,
    a.experience_months,
    a.shift

ORDER BY avg_quality ASC;

-- Analyzing monthly trends


SELECT
    strftime('%Y-%m', date) AS month,

    COUNT(*) AS tickets,

    ROUND(AVG(resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(csat), 2)
        AS avg_csat,

    ROUND(AVG(CAST(sla_met AS FLOAT)) * 100, 2)
        AS sla_compliance,

    ROUND(AVG(CAST(fcr AS FLOAT)) * 100, 2)
        AS fcr_rate

FROM support_tickets

GROUP BY strftime('%Y-%m', date)

ORDER BY month;

-- Finding bottlenecks

SELECT
    team,
    complexity,

    COUNT(*) AS ticket_count,

    ROUND(AVG(resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(CAST(sla_met AS FLOAT)) * 100, 2)
        AS sla_compliance,

    ROUND(AVG(CAST(reopened AS FLOAT)) * 100, 2)
        AS reopen_rate,

    ROUND(AVG(csat), 2)
        AS avg_csat

FROM support_tickets

GROUP BY team, complexity

ORDER BY avg_resolution_time DESC;

-- Comparing the changes


SELECT
    a.shift,

    COUNT(*) AS tickets,

    ROUND(AVG(t.resolution_time_min), 2)
        AS avg_resolution_time,

    ROUND(AVG(t.quality_score), 2)
        AS avg_quality,

    ROUND(AVG(CAST(t.sla_met AS FLOAT)) * 100, 2)
        AS sla_compliance,

    ROUND(AVG(t.csat), 2)
        AS avg_csat

FROM support_tickets t

JOIN agents a
    ON t.agent_id = a.agent_id

GROUP BY a.shift

ORDER BY sla_compliance ASC;

