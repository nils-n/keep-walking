function sum(a, b) {
  return a + b;
}

function getBMIstatus(current_bmi) {
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
