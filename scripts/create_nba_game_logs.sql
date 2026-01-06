CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS nba_game_logs (
  id BIGSERIAL PRIMARY KEY,
  game_date date NOT NULL,
  matchup text NOT NULL,
  player_name text NOT NULL,
  stats_summary text NOT NULL,
  search_text TEXT,
  embedding vector(768)
);