function sum(a, b) {
  return a + b;
}

function getBMIstatus(args) {
  if (args == null) {
    throw new Error("No arguments provided (expected 1)");
  }

  if (args.length > 1) {
    throw new Error("Too many arguments (expected 1)");
  }

  current_bmi = args;

  const lower_healthy_limit = 18.5;
  const upper_healthy_limit = 25.0;

  if (current_bmi > lower_healthy_limit && current_bmi < upper_healthy_limit) {
    return "just right";
  } else if (current_bmi > upper_healthy_limit) {
    return "too high";
  } else {
    return "too low";
  }
}

module.exports = {
  sum,
  getBMIstatus,
};
