/*jshint esversion: 6 */

function sum(a, b) {
  return a + b;
}

// function to evaluate whether the current BMI is in the
// healthy range  (or below/above this range)
function getBMIstatus(args) {
  if (args == null) {
    throw new Error("No arguments provided (expected 1)");
  }

  if (arguments.length > 1) {
    throw new Error("Too many arguments (expected 1)");
  }

  if (isNaN(args)) {
    throw new Error("Argument is not a number");
  }

  if (typeof args === "string") {
    throw new Error("Argument should not be a string");
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
// function to evaluate the trend of the current BMI
// this should indicate whether the BMI is currently
// improving,  getting worse, or staying same
function getBMItrend(args) {
  if (args == null) {
    throw new Error("No arguments provided (expected 1)");
  }

  if (args.length > 1) {
    throw new Error("Too many arguments (expected 1)");
  }

  current_bmi_change = args;

  const limit_for_increasing_trend = 0.25;
  const limit_for_decreasing_trend = -0.25;

  if (current_bmi_change < limit_for_decreasing_trend) {
    return "decreasing";
  } else if (current_bmi_change > limit_for_increasing_trend) {
    return "increasing";
  } else {
    return "constant";
  }
}

module.exports = {
  sum,
  getBMIstatus,
  getBMItrend,
};
