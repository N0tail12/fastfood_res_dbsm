var express = require("express");
var session = require("express-session");
var flash = require("connect-flash");
var multer = require("multer");
var app = express();
var cookieParser = require("cookie-parser");
let path = require("path");
app.use(express.json());
app.use(express.static("public"));
app.use("/css", express.static(__dirname + "/lib/bootstrap/css"));
app.use("/js", express.static(__dirname + "/lib/bootstrap/js"));
app.use("/views", express.static(__dirname + "/views"));
app.use("/img", express.static(__dirname + "/public/img"));
app.use("/css", express.static(__dirname + "/public/css"));
app.use("/js", express.static(__dirname + "/public/js"));
app.set("view engine", "ejs");
app.set("views", "./views");
app.listen(3000);

app.use(express.urlencoded({ extended: false }));
app.use(flash());
app.use(cookieParser("secretString"));

const { Pool } = require("pg");
const { render } = require("ejs");
const connectionString =
  "postgres://ijgbgbrz:UXX0MoGyaIw8cXPmUdHI5aWas3HHP5Oy@queenie.db.elephantsql.com:5432/ijgbgbrz";
const pool = new Pool({
  connectionString,
});
app.use(
  session({
    cookie: { maxAge: 60000 },
  })
);

let diskStorage = multer.diskStorage({
  destination: (req, file, callback) => {
    callback(null, "public/img");
  },
  filename: (req, file, callback) => {
    let math = ["image/png", "image/jpeg"];
    if (math.indexOf(file.mimetype) === -1) {
      let errorMess = `The file <strong>${file.originalname}</strong> is invalid. Only allowed to upload image jpeg or png.`;
      return callback(errorMess, null);
    }
    let filename = `${file.originalname}`;
    callback(null, filename);
  },
});

let uploadFile = multer({ storage: diskStorage });

//Main
app.get("/", function (req, res) {
  res.render("main");
});
//Sign In
app.post("/", async (req, res) => {
  let fname = req.body.signfname;
  let lnane = req.body.signlname;
  let email = req.body.signemail;
  let pass = req.body.signpass;
  let pnumber = req.body.signpnumber;
  let area = req.body.signarea;
  let town = req.body.signtown;
  try {
    let rs = await pool.query(
      "INSERT INTO customer_info VALUES ('" +
        email +
        "','" +
        fname +
        "','" +
        lnane +
        "','" +
        pass +
        "','" +
        pnumber +
        "','" +
        area +
        "','" +
        town +
        "','Active');"
    );
    req.flash("message", "Signup Success");
    req.flash("type", "success");
    res.render("main", {
      message: req.flash("message"),
      type: req.flash("type"),
    });
  } catch (err) {
    req.flash("message", "This Email is already taken, please try again");
    req.flash("type", "danger");
    res.render("main", {
      message: req.flash("message"),
      type: req.flash("type"),
    });
  }
});
//login
app.post("/home", async (req, res) => {
  var user = req.body.txtemail;
  var pass = req.body.pass;

  try {
    let rs = await pool.query(
      "Select * from customer_info where email = '" +
        user +
        "' and pass = '" +
        pass +
        "' and status = 'Active'"
    );
    if (rs.rowCount > 0) {
      res.redirect("/customer?user=" + user);
    } else {
      rs = await pool.query(
        "Select * from management where user_id = '" +
          user +
          "' and pass = '" +
          pass +
          "' and status = 'Actv'"
      );
      if (rs.rows[0].designation == "Manager") {
        res.redirect("/manager?user=" + user);
      } else if (
        rs.rows[0].designation == "Employee" ||
        rs.rows[0].designation == "Cook"
      ) {
        res.redirect(
          "/employee?user=" + user + "&designation=" + rs.rows[0].designation
        );
      }
    }
    req.session.isAuth = true;
    console.log(req.session);
  } catch (err) {
    req.flash("message", "Login Failed. Try again!");
    req.flash("type", "danger");
    res.render("main", {
      message: req.flash("message"),
      type: req.flash("type"),
    });
  }
});

// Manager Functions
app.get("/manager", async (req, res) => {
  let remember = req.query.user;
  let rs = await pool.query(
    "select * from management where user_id = '" + remember + "'"
  );
  const info = rs.rows[0];
  console.log(info);
  res.render("manager", { remember: remember, info: info });
});
app.post("/manager", async (req, res) => {
  let user_id = req.body.management_id;
  let user_name = req.body.management_name;
  let rs = await pool.query(
    "update management set user_name = '" +
      user_name +
      "' where user_id = '" +
      user_id +
      "'"
  );
  res.redirect("/manager?user=" + user_id);
});
//Customer Information Function
app.get("/manager/customerinfo", async (req, res) => {
  let rs = await pool.query("Select * from customer_info");
  let page = req.query.page;
  let remember = req.query.user;
  let limit = 20;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);

  res.render("customerinfo", {
    info: info,
    page: page,
    numberpage: rs.rowCount / limit,
    remember: remember,
  });
});

app.get("/manager/customerinfo/top10", async (req, res) => {
  let rs = await pool.query(
    "select cus.email ,cus.fname||' '||cus.lname as name, cus.phone, cus.town, cus.area, sum(quantity) as total_num\
  from order_info as oi, order_items as ot, customer_info as cus\
  where oi.order_id = ot.order_id and ot.status != 'Cancel'  and cus.email = oi.email\
  group by(cus.email)\
  order by(total_num) desc\
  limit 10"
  );
  let page = req.query.page;
  let remember = req.query.user;
  let limit = 20;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);

  res.render("top10", {
    info: info,
    page: page,
    numberpage: rs.rowCount / limit,
    remember: remember,
  });
});

app.get("/manager/customerinfo/familiar", async (req, res) => {
  let rs = await pool.query(
    "select cus.email,cus.fname||' '||cus.lname as name, cus.phone, cus.area, cus.town, count(o.email) from order_info o, customer_info cus where o.email = cus.email group by o.email,cus.email having count(o.email)>3 and max('TORCV') > '2020-12-31'"
  );
  let page = req.query.page;
  let remember = req.query.user;
  let limit = 20;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);

  res.render("familiar", {
    info: info,
    page: page,
    numberpage: rs.rowCount / limit,
    remember: remember,
  });
});
// Employee Information Function
app.get("/manager/employeeinfo", async (req, res) => {
  let rs = await pool.query("select * from management");
  let page = req.query.page;
  let remember = req.query.user;
  let limit = 20;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);

  res.render("employeeinfo", {
    info: info,
    page: page,
    numberpage: rs.rowCount / limit,
    remember: remember,
  });
});

app.post("/addemployee", async (req, res) => {
  let username = req.body.empusername;
  let pass = req.body.emppass;
  let name = req.body.empname;
  let design = req.body.design;
  let remember = req.body.hidden;
  // let rs = await pool.query("INSERT INTO management VALUES ('"+username+"','"+pass+"','"+name+"','Actv','"+design+"');")
  try {
    let rs = await pool.query(
      "INSERT INTO management VALUES ('" +
        username +
        "','" +
        pass +
        "','" +
        name +
        "','Actv','" +
        design +
        "');"
    );
    res.redirect("/manager/employeeinfo?page=1&user=" + remember);
  } catch (error) {
    res.send("<p> Failed </p>");
  }
});

app.post("/changeemployee", async (req, res) => {
  let userid = req.body.chuserid;
  let name = req.body.chpname;
  let design = req.body.chdesign;
  let remember = req.body.hidden;
  let rs = await pool.query(
    "update management set user_name = '" +
      name +
      "', designation ='" +
      design +
      "' where user_id='" +
      userid +
      "'"
  );
  res.redirect("/manager/employeeinfo?page=1&user=" + remember);
});

app.get("/manager/deleteemployee", async (req, res) => {
  let user_id = req.query.user_id;
  let remember = req.query.user;
  let rs = await pool.query(
    "delete from management where user_id = '" + user_id + "'"
  );
  res.redirect("/manager/employeeinfo?page=1&user=" + remember);
});
// Menu Information Function

app.get("/manager/menu", async (req, res) => {
  let rs = await pool.query("select * from menu");

  function compare(a, b) {
    if (parseInt(a.item_id) < parseInt(b.item_id)) {
      return -1;
    }
    if (parseInt(a.item_id) > parseInt(b.item_id)) {
      return 1;
    }
    return 0;
  }
  rs.rows.sort(compare);
  console.log(rs.rows);
  let page = req.query.page;
  let remember = req.query.user;
  let limit = 20;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);
  res.render("menu", {
    info: info,
    page: page,
    numberpage: rs.rowCount / limit,
    remember: remember,
  });
});

app.post("/addmenu", uploadFile.single("chpic"), async (req, res) => {
  let id = req.body.menuid;
  let name = req.body.menuname;
  let price = req.body.menuprice;
  let category = req.body.category;
  let remember = req.body.hidden;
  let dir = "img/" + req.file.filename;
  console.log(dir);
  console.log(req.body, req.file);
  try {
    let rs = await pool.query(
      "INSERT INTO menu VALUES ('" +
        id +
        "','" +
        name +
        "','" +
        dir +
        "','" +
        price +
        "','" +
        category +
        "','Available','mhieu345');"
    );
    res.redirect("/manager/menu?page=1&user=" + remember);
  } catch (error) {
    res.redirect(406, "/manager/menu?page=1&user=" + remember);
  }
});
app.get("/manager/deletemenu", async (req, res) => {
  let id = req.query.id;
  let remember = req.query.user;
  let rs = await pool.query("delete from menu where item_id = '" + id + "'");
  res.redirect("/manager/menu?page=1&user=" + remember);
});

app.post("/changemenu", async (req, res) => {
  let id = req.body.chid;
  let name = req.body.chname;
  let price = req.body.chprice;
  let category = req.body.chcategory;
  let status = req.body.status;
  let remember = req.body.hidden;
  let rs = await pool.query(
    "update menu set item_name = '" +
      name +
      "', price = '" +
      price +
      "', catagory = '" +
      category +
      "', status = '" +
      status +
      "' where item_id = '" +
      id +
      "'"
  );
  res.redirect("/manager/menu?page=1&user=" + remember);
});

//Sale Function
app.get("/manager/sale", async (req, res) => {
  res.render("sale", { remember: req.query.user });
});
app.post("/manager/sale", async (req, res) => {
  let page = req.body.page;
  let dateStart = req.body.dateStart;
  let dateEnd = req.body.dateEnd;
  let rs = await pool.query(
    "select oi.todel, sum(me.price * ot.quantity) as total\
    from menu as me, order_items  as ot, order_info as oi\
    where me.item_id = ot.item_id and ot.order_id = oi.order_id\
    and todel between '" +
      dateStart +
      "' and '" +
      dateEnd +
      "' and ot.status != 'Cancel'\
    group by(todel)\
    order by(todel)"
  );
  // let limit = 20;
  // if (page < 1) page = 1;
  // if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  // const startIndex = (page - 1) * limit;
  // const endIndex = page * limit;
  // const info = rs.rows.slice(startIndex, endIndex);
  // console.log(info);
  const info = rs.rows;
  res.json({ sale: info });
});
// Customer Function
app.get("/customer", async (req, res) => {
  let rs = await pool.query("select * from menu");
  function compare(a, b) {
    if (parseInt(a.item_id) < parseInt(b.item_id)) {
      return -1;
    }
    if (parseInt(a.item_id) > parseInt(b.item_id)) {
      return 1;
    }
    return 0;
  }
  rs.rows.sort(compare);
  res.render("customer", { info: rs.rows });
});
app.get("/customer/profile", async (req, res) => {
  let user_id = req.query.user;
  let rs = await pool.query(
    "select * from customer_info where email = '" + user_id + "'"
  );
  res.render("myProfile", { info: rs.rows[0] });
  // res.json(rs.rows[0]);
});
app.post("/customer/profile", async (req, res) => {
  let email = req.body.customer_email;
  let phoneNumber = req.body.customer_phone;
  let area = req.body.customer_area;
  let town = req.body.customer_town;
  let rs = await pool.query(
    "update customer_info set phone = '" +
      phoneNumber +
      "', area = '" +
      area +
      "', town = '" +
      town +
      "' where email = '" +
      email +
      "'"
  );
  res.redirect("/customer/profile?user=" + email + "&page=1");
});
//Employee Function
app.get("/employee", async (req, res) => {
  let user = req.query.user;
  try {
    let rs = await pool.query(
      "select * from management where user_id = '" + user + "'"
    );
    console.log(rs.rows[0]);
    res.render("employee", { info: rs.rows[0] });
  } catch (error) {
    console.log(error);
  }
});
app.post("/employee", async (req, res) => {
  let user_id = req.body.management_id;
  let user_name = req.body.management_name;
  try {
    let rs = await pool.query(
      "update management set user_name = '" +
        user_name +
        "' where user_id = '" +
        user_id +
        "'"
    );
    res.redirect("/employee?user=" + user_id);
  } catch (error) {
    console.log(error);
  }
});
app.get("/employee/order", (req, res) => {
  let remember = req.query.user;
  let designation = req.query.designation;
  res.render("order", { remember: remember, designation: designation });
});
//some api
app.get("/getOrderId", async (req, res) => {
  let rs = await pool.query("select order_id from order_info");
  function compare(a, b) {
    if (parseInt(a.order_id) < parseInt(b.order_id)) {
      return -1;
    }
    if (parseInt(a.order_id) > parseInt(b.order_id)) {
      return 1;
    }
    return 0;
  }
  rs.rows.sort(compare);
  res.json(rs.rows[rs.rows.length - 1]);
});
app.post("/rainbow", async (req, res) => {
  try {
    let getCooker = await pool.query(
      "select user_id\
      from management\
      where status != 'Blkd' and user_id in (\
      select user_id\
      from order_items\
      where status = 'Pending'\
      group by(user_id)\
      order by(count(*))\
      limit 1)"
    );
    let insertInfo = await pool.query(
      "insert into order_info values('" +
        req.body.order_id +
        "','" +
        req.body.user_id +
        "','" +
        req.body.torcv +
        "','" +
        req.body.todel +
        "')"
    );
    let insertItems = await pool.query(
      "insert into order_items values('" +
        req.body.order_id +
        "','" +
        req.body.item_id +
        "','" +
        req.body.quantity +
        "', 'Pending', '" +
        getCooker.rows[0].user_id +
        "')"
    );
    console.log(getCooker.rows[0].user_id);
    res.json({ result: true });
  } catch {
    console.log("Something Wrong!");
    res.json({ result: false });
  }
});
app.post("/getAllOrder", async (req, res) => {
  let email = req.body.email;
  let page = req.body.page;
  let rs = await pool.query(
    "select ot.order_id as order_id, item_name, quantity,\
    torcv as order_date, todel as order_del,\
    ot.status as status from order_info oi,\
    order_items ot, menu n\
    where oi.order_id = ot.order_id and ot.item_id = n.item_id and email = '" +
      email +
      "';"
  );
  function compare(a, b) {
    if (parseInt(a.order_id) < parseInt(b.order_id)) {
      return -1;
    }
    if (parseInt(a.order_id) > parseInt(b.order_id)) {
      return 1;
    }
    return 0;
  }
  rs.rows.sort(compare);
  let limit = 10;
  if (page < 1) page = 1;
  if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const info = rs.rows.slice(startIndex, endIndex);
  res.json({ order: info, pageNumber: Math.ceil(rs.rowCount / limit) });
});
app.post("/cancelOrder", async (req, res) => {
  let id = req.body.order_id;
  try {
    let rs = await pool.query(
      "update order_items set status = 'Cancel' where order_id = '" + id + "'"
    );
    res.json({ result: true });
  } catch {
    res.json({ result: false });
  }
});
app.post("/checkCustomerPassword", async (req, res) => {
  let pass = req.body.password;
  let email = req.body.email;
  try {
    let rs = await pool.query(
      "select * from customer_info where email = '" +
        email +
        "' and pass = '" +
        pass +
        "'"
    );
    console.log(rs.rowCount);
    if (rs.rowCount) res.json({ result: true });
    else res.json({ result: false });
  } catch (error) {
    console.log(error);
  }
});
app.post("/changeCustomerPassword", async (req, res) => {
  let pass = req.body.password;
  let email = req.body.email;
  try {
    let rs = await pool.query(
      "update customer_info set pass = '" +
        pass +
        "' where email = '" +
        email +
        "'"
    );
    res.json({ result: true });
  } catch (error) {
    console.log(error);
    res.json({ result: false });
  }
});
app.post("/checkManagementPassword", async (req, res) => {
  console.log(req.body);
  let pass = req.body.password;
  let user_id = req.body.user_id;
  try {
    let rs = await pool.query(
      "select * from management where user_id = '" +
        user_id +
        "' and pass = '" +
        pass +
        "'"
    );
    if (rs.rowCount) res.json({ result: true });
    else res.json({ result: false });
  } catch (error) {
    console.log(error);
  }
});
app.post("/changManagementPassword", async (req, res) => {
  let pass = req.body.password;
  let user_id = req.body.user_id;
  try {
    let rs = await pool.query(
      "update management set pass = '" +
        pass +
        "' where user_id = '" +
        user_id +
        "'"
    );
    res.json({ result: true });
  } catch (error) {
    console.log(error);
    res.json({ result: false });
  }
});
app.post("/employeeOrder", async (req, res) => {
  let page = req.body.page;
  try {
    let rs = await pool.query(
      "select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
      from order_info, order_items \
      where order_info.order_id = order_items.order_id and order_items.status = 'Ready'"
    );
    let limit = 25;
    if (page < 1) page = 1;
    if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    const info = rs.rows.slice(startIndex, endIndex);
    console.log(info);
    res.json({ order: info, pageNumber: Math.ceil(rs.rowCount / limit) });
  } catch (error) {
    console.log(error);
  }
});
app.post("/cookerOrder", async (req, res) => {
  let page = req.body.page;
  let user = req.body.user_id;
  try {
    let rs = await pool.query(
      "select order_info.order_id, email, item_id, quantity, status, user_id, torcv, todel\
      from order_info, order_items \
      where order_info.order_id = order_items.order_id and user_id = '" +
        user +
        "'"
    );
    let limit = 25;
    if (page < 1) page = 1;
    if (page > rs.rowCount / limit) page = Math.ceil(rs.rowCount / limit);
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    const info = rs.rows.slice(startIndex, endIndex);
    console.log(info);
    res.json({ order: info, pageNumber: Math.ceil(rs.rowCount / limit) });
  } catch (error) {
    console.log(error);
  }
});
app.post("/complete", async (req, res) => {
  let id = req.body.order_id;
  try {
    let rs = await pool.query(
      "update order_items set status = 'Ready' where order_id = '" + id + "'"
    );
    res.json({ result: true });
  } catch (error) {
    console.log(error);
    res.json({ result: false });
  }
});
app.post("/checkID", async (req, res) => {
  let item_id = req.body.item_id;
  try {
    let rs = await pool.query(
      "select * from menu where item_id = '" + item_id + "'"
    );
    if (!rs.rowCount) {
      res.json({ result: true });
    } else {
      res.json({ result: false });
    }
  } catch (error) {}
});
app.post("/checkUser", async (req, res) => {
  let user_id = req.body.user_id;
  try {
    let rs = await pool.query(
      "select * from management where user_id = '" + user_id + "'"
    );
    if (!rs.rowCount) {
      res.json({ result: true });
    } else {
      res.json({ result: false });
    }
  } catch (error) {}
});
