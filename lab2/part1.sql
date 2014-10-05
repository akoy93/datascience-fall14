# Problem 1
SELECT * 
  FROM results r
  WHERE r.event_id = (
    SELECT event_id
    FROM events
    WHERE name = '110m Hurdles Men' AND olympic_id = 'SYD2000');

# Problem 2
SELECT COUNT(*)
  FROM players
  WHERE SUBSTR(name, 0, 2) IN ('A', 'E', 'I', 'O', 'U');

# Problem 3
SELECT COUNT(*)
  FROM events
  WHERE result_noted_in = 'points';

# Problem 4

WITH players_2000 AS (
    SELECT DISTINCT p.* 
    FROM players p, events e, results r
    WHERE p.player_id = r.player_id AND r.event_id = e.event_id AND e.olympic_id = 'SYD2000'
  ), results_2000 AS (
    SELECT r.*
    FROM results r, events e
    WHERE r.event_id = e.event_id AND e.olympic_id = 'SYD2000'
  ), team_medals AS (
    SELECT country_id, r.event_id, medal, result
    FROM results_2000 r, players_2000 p, events e
    WHERE r.player_id = p.player_id AND r.event_id = e.event_id AND e.is_team_event = 1
    GROUP BY r.event_id, country_id, medal, result
    ORDER BY r.event_id, result
  ), team_medal_count AS (
    SELECT a.country_id, COALESCE(count, 0) as count
    FROM (SELECT country_id FROM countries) as a
    LEFT JOIN (SELECT country_id, COUNT(*)
                FROM team_medals
                GROUP BY country_id) as b
    ON a.country_id = b.country_id
  ), individual_medals AS (
    SELECT i.*
    FROM individualmedals i
    INNER JOIN results_2000 r
    ON i.event_id = r.event_id AND i.player_id = r.player_id
  ), individual_medal_count AS (
    SELECT a.country_id, COALESCE(count, 0) as count
    FROM (SELECT country_id FROM countries) as a
    LEFT JOIN (SELECT country_id, COUNT(*)
                FROM individual_medals
                GROUP BY country_id) as b
    ON a.country_id = b.country_id
  ), medal_count AS (
    SELECT t.country_id, (t.count + i.count) AS num_medals
    FROM team_medal_count t, individual_medal_count i
    WHERE t.country_id = i.country_id
  )
SELECT m.country_id, (CAST(num_medals AS float) / CAST(population AS float)) AS "number-of-medals/population"
  FROM medal_count m, countries c
  WHERE m.country_id = c.country_id
  ORDER BY "number-of-medals/population" ASC
  LIMIT 5;

# Problem 5
WITH num_players AS (
  SELECT COUNT(*) AS num_players, country_id
    FROM players
    GROUP BY country_id
  )
  SELECT name AS country_name, num_players
  FROM countries c, num_players n
  WHERE c.country_id = n.country_id;

# Problem 6
SELECT *
  FROM players
  WHERE RIGHT(name, 1) = 'd'
  ORDER BY country_id ASC, birthdate DESC;

# Problem 7
WITH players_2004 AS (
    SELECT DISTINCT p.* 
    FROM players p, events e, results r
    WHERE p.player_id = r.player_id AND r.event_id = e.event_id AND e.olympic_id = 'ATH2004'
  ), results_2004 AS (
    SELECT r.*
    FROM results r, events e
    WHERE r.event_id = e.event_id AND e.olympic_id = 'ATH2004'
  ), num_players AS (
    SELECT EXTRACT(year FROM birthdate) AS birthyear, COUNT(p.*) AS "num-players"
    FROM players_2004 p
    GROUP BY birthyear
  ), num_gold_medals AS (
    SELECT EXTRACT(year FROM birthdate) AS birthyear, COUNT(r.*) AS "num-gold-medals"
    FROM players_2004 p, results_2004 r
    WHERE r.medal = 'GOLD' AND p.player_id = r.player_id
    GROUP BY birthyear
  )
SELECT p.birthyear, "num-players", "num-gold-medals"
  FROM num_players p, num_gold_medals g
  WHERE p.birthyear = g.birthyear
  ORDER BY p.birthyear;

# Problem 8
WITH individual_events AS (
    SELECT r.*
    FROM results r, events e
    WHERE r.event_id = e.event_id AND e.is_team_event = 0
  ), tied_events AS (
    SELECT COUNT(medal) AS gold_medal_count, event_id
    FROM individual_events i
    WHERE i.medal = 'GOLD'
    GROUP BY event_id
    HAVING COUNT(medal) >= 2
  )
SELECT * FROM tied_events;

# Problem 9
WITH butterfly_events AS (
    SELECT *
    FROM events
    WHERE name LIKE '%Butterfly%' AND olympic_id = 'ATH2004'
  ), gold_times AS (
    SELECT r.*
    FROM results r, butterfly_events b
    WHERE r.event_id = b.event_id AND medal = 'GOLD'
  ), silver_times AS (
    SELECT r.*
    FROM results r, butterfly_events b
    WHERE r.event_id = b.event_id AND medal = 'SILVER'
  )
SELECT s.event_id, (s.result - g.result) AS difference
  FROM silver_times s, gold_times g
  WHERE s.event_id = g.event_id;

# Problem 10
CREATE table TeamMedals AS
  SELECT country_id, r.event_id, medal, result
    FROM results r, players p, events e
    WHERE r.player_id = p.player_id AND r.event_id = e.event_id AND e.is_team_event = 1
    GROUP BY r.event_id, country_id, medal, result
    ORDER BY r.event_id, result;

# Problem 11
SELECT a.name, COALESCE(count, 0)
  FROM (SELECT name FROM countries) as a
  LEFT JOIN (SELECT c.name, COUNT(p.name)
          FROM countries c
          LEFT OUTER JOIN players p
          ON c.country_id = p.country_id
          WHERE EXTRACT(year FROM p.birthdate) = 1975
          GROUP BY c.name) AS b
  ON a.name = b.name;
