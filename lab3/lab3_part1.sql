-- 1
CREATE VIEW NumberOfMedals AS
SELECT name AS country_name, num_medals AS number_of_medals
  FROM countries
  INNER JOIN
  (SELECT country_id, COUNT(*) AS num_medals
    FROM ( SELECT DISTINCT country_id, event_id, medal
        FROM results r
        INNER JOIN players p
        ON r.player_id = p.player_id) AS country_medals
    GROUP BY country_id) AS country_counts
  ON countries.country_id = country_counts.country_id
  ORDER BY name;

-- 2
SELECT a, b, R.c, d
  FROM R
  INNER JOIN S
  ON (R.C = S.C) OR (R.C IS NULL AND S.C IS NULL);

SELECT a, b, R.c, d
  FROM R
  FULL OUTER JOIN S
  ON R.C = S.C
  WHERE R.c IS NULL;

-- 3
CREATE OR REPLACE FUNCTION update_team_medals()
  RETURNS trigger AS
$$
DECLARE
  country_id text;
BEGIN
  IF NEW.event_id IN (SELECT event_id FROM events WHERE is_team_event = 1) THEN
    country_id = (SELECT p.country_id FROM players p WHERE NEW.player_id = player_id);
    INSERT INTO TeamMedals
    VALUES(country_id, NEW.event_id, NEW.medal, NEW.result);
  END IF;

  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql' VOLATILE;

CREATE TRIGGER add_result
  BEFORE INSERT 
  ON results
  FOR EACH ROW
  EXECUTE PROCEDURE update_team_medals();

SELECT * 
  FROM TeamMedals
  WHERE country_id = 'USA';

DELETE FROM results
  WHERE medal = 'GOLD' AND event_id = 'E81';

INSERT INTO results 
  VALUES('E81', 'JONESMAR03', 'GOLD', '193.11'),
        ('E81', 'GREENMAU01', 'GOLD', '193.11'),
        ('E81', 'KEFLEMEB01', 'GOLD', '193.11'),
        ('E81', 'JOHNSMIC01', 'GOLD', '193.11');

-- 4
CREATE OR REPLACE FUNCTION list_gold_medals()
  RETURNS text AS
$$
  DECLARE
    prev_name text;
    curr record;
    result text;
    closed integer;
  BEGIN
    result := '';
    prev_name := '';
    closed := 1;

    FOR curr IN
      (SELECT event_name, name AS player_name
        FROM 
          (SELECT e.event_id, name as event_name, medal, player_id
           FROM (SELECT * FROM events WHERE olympic_id = 'ATH2004') e
           INNER JOIN (SELECT * FROM results WHERE medal = 'GOLD') r
           ON e.event_id = r.event_id) AS res
        INNER JOIN players p
        ON p.player_id = res.player_id
        WHERE country_id = 'USA')
    LOOP
      IF prev_name <> TRIM(curr.event_name) AND closed = 0 THEN
        result := result || '</medal>' || E'\n';
        closed := 1;
      END IF;

      IF prev_name <> TRIM(curr.event_name) AND closed = 1 THEN
        result := result || '<medal>' || E'\n';
        result := result || '  <event>' || curr.event_name || '</event>' || E'\n';
        closed := 0;
      END IF;

      result := result || '  <player>' || curr.player_name || '</player>' || E'\n';

      prev_name := TRIM(curr.event_name);
    END LOOP;

    IF closed = 0 THEN
      result := result || '</medal>' || E'\n';
    END IF;

    RETURN result;
  END;
$$
LANGUAGE 'plpgsql' IMMUTABLE;








