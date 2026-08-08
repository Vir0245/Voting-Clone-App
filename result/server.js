const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = process.env.PORT || 80;

const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'postgres',
  port: 5432,
});

app.set('view engine', 'pug');
app.use(express.static('public'));

app.get('/', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT vote, COUNT(*) AS count FROM votes GROUP BY vote'
    );

    let votesA = 0, votesB = 0;
    result.rows.forEach(row => {
      if (row.vote === 'a') votesA = parseInt(row.count);
      if (row.vote === 'b') votesB = parseInt(row.count);
    });

    const total = votesA + votesB;
    const percentA = total > 0 ? Math.round((votesA / total) * 100) : 0;
    const percentB = total > 0 ? Math.round((votesB / total) * 100) : 0;

    res.render('index', { 
      votesA, votesB, total, percentA, percentB,
      optionA: process.env.OPTION_A || 'Pizza',
      optionB: process.env.OPTION_B || 'Burger'
    });
  } catch (err) {
    console.error(err);
    res.render('index', { 
      votesA: 0, votesB: 0, total: 0, percentA: 0, percentB: 0,
      optionA: process.env.OPTION_A || 'Pizza',
      optionB: process.env.OPTION_B || 'Burger'
    });
  }
});

app.listen(port, () => {
  console.log(`Result app listening on port ${port}`);
});
