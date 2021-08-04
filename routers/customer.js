const express = require('express')
const { Pool } = require('pg');
const cus = express();
const connectionString = 'postgres://ijgbgbrz:UXX0MoGyaIw8cXPmUdHI5aWas3HHP5Oy@queenie.db.elephantsql.com:5432/ijgbgbrz'
const pool = new Pool({
  connectionString,
})