const express = require("express");
const bodyParser = require("body-parser");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const app = express();
const PORT = 5500;
const secretKey = "ashwin123anto";


app.use(bodyParser.json());


const users = [
  { id: 1, username: "user1", password: bcrypt.hashSync("password1", 10), role: "user" },
  { id: 2, username: "user2", password: bcrypt.hashSync("password2", 10), role: "admin" },
];


app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username);

  if (!user) {
    return res.status(401).json({ message: "invalid creds" });
  }

  const isPasswordValid = await bcrypt.compare(password, user.password);
  if (!isPasswordValid) {
    return res.status(401).json({ message: "invalid creds" });
  }


  const token = jwt.sign({ userId: user.id, role: user.role }, secretKey, { expiresIn: "2h" });
  res.json({ token });
});


app.post("/register", async (req, res) => {
  const { username, password, role } = req.body;
  const existingUser = users.find(u => u.username === username);

  if (existingUser) {
    return res.status(400).json({ message: "Username exists" });
  }

  
  const hashedPassword = await bcrypt.hash(password, 10);


  const newUser = { id: users.length + 1, username, password: hashedPassword, role: role || 'user' };
  users.push(newUser);

  res.status(201).json({ message: "User register success" });
});


function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  jwt.verify(token, secretKey, (err, user) => {
    if (err) {
      return res.status(403).json({ message: "Invalid token" });
    }
    req.user = user;
    next();
  });
}


function authorizeRole(role) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ message: "Forbidden" });
    }
    next();
  };
}


app.get("/protected", authenticateToken, (req, res) => {
  res.json({ message: "Protected route accessed successfully!" });
});

app.get("/admin", authenticateToken, authorizeRole("admin"), (req, res) => {
  res.json({ message: "Admin route accessed successfully!" });
});

app.get("/user", authenticateToken, (req, res) => {
  res.json({ message: "User route accessed successfully!" });
});


app.listen(PORT, () => {
  console.log('Server is running');
});