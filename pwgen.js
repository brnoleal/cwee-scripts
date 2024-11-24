var length = process.argv[2];
var type = process.argv[3];

if (length === undefined || type === undefined) {
  console.log("usage: node pwgen.js <length> <type>");
  console.log("length: integer between 8 and 128");
  console.log("type: simple or complex");
}

function generatePassword(length, type) {
  let password = "";
  let characters =
    type === "simple"
      ? "abcdefghijklmnopqrstuvwxyz"
      : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()";

  for (let i = 0; i < length; i++) {
    password += characters.charAt(
      Math.floor(Math.random() * characters.length)
    );
  }

  new Function(
    `console.log("${type} password - length ${length}: ${password}")`
  )();
}

try {
  generatePassword(length, type);
} catch (e) {
  console.log(e);
}

module.exports = {
  generatePassword,
};
