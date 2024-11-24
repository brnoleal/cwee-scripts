var length = process.argv[2];
var type = process.argv[3];

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

  if (length === undefined || type === undefined) {
    console.log("usage: node pwgen.js <length> <type>");
    console.log("length: integer between 8 and 128");
    console.log("type: simple or complex");
  }

  // Throw an error if length is not an integer
  if (!Number.isInteger(Number(length))) {
    throw new Error("Length must be an integer.");
  }

  // Remove any non-digit characters from length 
  length = length ? length.replace(/\D/g, '') : undefined;

  // Remove any non-alphanumeric characters from type 
  type = type ? type.replace(/[^a-zA-Z0-9]/g, '') : undefined;

  generatePassword(length, type);
} catch (e) {
  console.log(e);
}

module.exports = {
  generatePassword,
};
