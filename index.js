var express = require("express");
var bodyParser = require("body-parser");
var session = require("express-session");
var flash = require('connect-flash');
var app = express();
var cookieParser = require('cookie-parser');
var items
app.use(express.static("public"));
app.use('/css', express.static(__dirname + '/lib/bootstrap/css'));
app.use('/js', express.static(__dirname + '/lib/bootstrap/js'));
// app.use('/JOEY2.png', express.static(__dirname + '/views/JOEY2.png'));
// app.use('/hamburger.jpg', express.static(__dirname + '/views/hamburger.jpg'));
// app.use('/pizza.jpg', express.static(__dirname + '/views/pizza.jpg'));
// app.use('/background.jpg', express.static(__dirname + '/views/background.jpg'));
//app.use('/style.css', express.static(__dirname + '/public/css/style.css'));
app.use('/views', express.static(__dirname + '/views'));
app.use('/img', express.static(__dirname + '/public/img'));
app.use('/css', express.static(__dirname + '/public/css'));
app.use('/js', express.static(__dirname + '/public/js'))
app.set("view engine", "ejs");
app.set("views", "./views");
app.listen(3000);

app.use(express.urlencoded({ extended: false }));
app.use(flash());
app.use(cookieParser('secretString'));
app.use(session({ cookie: { maxAge: 60 } }));

const { Pool } = require('pg');
const connectionString = 'postgres://ijgbgbrz:UXX0MoGyaIw8cXPmUdHI5aWas3HHP5Oy@queenie.db.elephantsql.com:5432/ijgbgbrz'
const pool = new Pool({
  connectionString,
})
app.get('/manager',(req,res)=>{
  res.render('manager')
})

app.get('/manager/customerinfo', async (req, res) => {
  let rs = await pool.query("Select * from customer_info");
  let page = req.query.page;
  let limit = 60
  if(page < 1)
  page = 1;
  if(page > (rs.rowCount/limit))
  page = Math.ceil(rs.rowCount/limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page*limit;
  const info = rs.rows.slice(startIndex, endIndex);
  // console.log(rs.rows)
  // let rs = await pool.query('select * from menu');
  // items = res.json(rs.rows);  
  res.render('customerinfo', {info: info, page: page, numberpage: rs.rowCount/limit})
});
app.get('/customer', (req,res)=>{

  res.render('customer')
})
// app.get('/manager',async (req,res)=>{
//   let rs = await pool.query('select * from menu')
//   items = res.json(rs.rows)
// })


app.get('/', function (req, res) {
  res.render("main");
});

app.post('/', async (req, res) => {
  let fname = req.body.signfname;
  let lnane = req.body.signlname;
  let email = req.body.signemail;
  let pass = req.body.signpass;
  let pnumber = req.body.signpnumber;
  let area = req.body.signarea;
  let town = req.body.signtown;
  try {
    let rs = await pool.query("INSERT INTO customer_info VALUES ('" + email + "','" + fname + "','" + lnane + "','" + pass + "','" + pnumber + "','" + area + "','" + town + "','Active');")
    req.flash('message', 'Signup Success')
    req.flash('type', 'success')
    res.render('main', { message: req.flash('message'), type: req.flash('type') });
    // console.log("oke");
  } catch (err) {
    req.flash('message', 'This Email is already taken, please try again')
    req.flash('type', 'danger')
    res.render('main', { message: req.flash('message'), type: req.flash('type') });
  }
});



app.post('/home', async (req, res) => {
  var user = req.body.txtemail;
  var pass = req.body.pass;
  // console.log(user);
  // console.log(pass);
  try {
    let rs = await pool.query("Select * from customer_info where email = '" + user + "' and pass = '" + pass + "' and status = 'Active'")
    if (rs.rowCount > 0) {
      res.cookie('user', 'cookie')
      res.redirect('/customer?user=' + user + '&page=1')
      // items = res.json(rs.rows)
      //res.render('customer',message);
    }
    else {
      rs = await pool.query("Select * from management where user_id = '" + user + "' and pass = '" + pass + "' and status = 'Actv'");
      if (rs.rows[0].designation == 'Manager') {
        res.redirect('/manager?user='+ user);
      }
      else if (rs.rows[0].designation == 'Employee' || rs.rows[0].designation == 'Cook') {
        req.flash('message', 'Login Success')
        req.flash('type', 'success')
        res.render('employee', { message: req.flash('message'), type: req.flash('type') });
      }
    }
  } catch (err) {
    req.flash('message', 'Login Failed. Try again!')
    req.flash('type', 'danger')
    res.render('main', { message: req.flash('message'), type: req.flash('type') });
  }
});


// app.get('/login', function(req, res){
//     res.render("login.ejs");
// })



module.exports = items;
