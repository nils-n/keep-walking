console.log("entering summary.js now...");

console.log("the answer is probably ...... " + sum(32, 10));
console.log("   A BMI of   16 is -->  " + getBMIstatus(16));
console.log("   A BMI of   20 is -->  " + getBMIstatus(20));
console.log("   A BMI of   28  is -->  " + getBMIstatus(28));

//: Good job. Your BMI is <span id='average-bmi'>{{ average_bmi }}
//</span>. Over the last month,
//you have maintained a healthy BMI and it has even improved by {{ change_bmi }}. Keep on walking!

function createBmiSummaryMessage(avg_bmi, change_bmi) {
  console.log("entering the function");

  // first assess whether BMI is currently too high, too low, or just right
  bmi_status = getBMIstatus(avg_bmi);
  bmi_trend = getBMItrend(change_bmi);

  // first create a summary message about the general BMI status
  let bmi_general_message;
  // case 1 : BMI too high
  if (bmi_status === "too high") {
    bmi_general_message = `Your BMI is ${avg_bmi}, that is too high.`;

    if (bmi_trend === "decreasing") {
      bmi_general_message += ` But you are on a good way! Over the last month, your BMI decreased by ${change_bmi}. Keep walking!`;
    } else if (bmi_trend === "constant") {
      bmi_general_message += ` Also, your BMI did not change much (${change_bmi}). Keep walking!`;
    } else {
      bmi_general_message += ` Your BMI got worse ( ${change_bmi}). Go out and walk, now is the best time!  `;
    }
    // case 2 : BMI in healthy range
  } else if (bmi_status === "just right") {
    bmi_general_message = `Your BMI is ${avg_bmi}, that is great!`;

    if (bmi_trend === "decreasing") {
      bmi_general_message += ` Your BMI decreased by ${change_bmi}. Keep walking (but not too much)!`;
    } else if (bmi_trend === "constant") {
      bmi_general_message += ` Good job! Your BMI changed only by ${change_bmi}. Keep walking!`;
    } else {
      bmi_general_message += ` Your BMI  increasing ( ${change_bmi}), keep that in mind. But also: Keep walking!`;
    }
    // case 3 : BMI too low
  } else {
    bmi_general_message = `Your BMI is ${avg_bmi}, that is too low.`;

    if (bmi_trend === "decreasing") {
      bmi_general_message += ` Your BMI decreased by ${change_bmi}. Be careful and watch your habits.`;
    } else if (bmi_trend === "constant") {
      bmi_general_message += ` Your BMI changed only slight ${change_bmi}. Keep walking, it will get better!`;
    } else {
      bmi_general_message += `Good job! Your BMI is increasing ( ${change_bmi}). Keep walking!`;
    }
  }

  return bmi_general_message;
}

// update the summary text based on the average BMI and change over the last month
document.addEventListener("DOMContentLoaded", function (event) {
  // extract the BMI and its change as it was passed from the View
  const average_bmi = parseFloat(
    document.getElementById("average-bmi").textContent,
  );
  const change_bmi = parseFloat(
    document.getElementById("change-bmi").textContent,
  );
  const bmi_message = document.getElementById("bmi-message");

  // apply some logic to create a summary message
  const updated_bmi_message = createBmiSummaryMessage(average_bmi, change_bmi);

  //enter the summary message into the DOM
  document.getElementById("bmi-message").textContent = updated_bmi_message;

  console.log("OK starting to adapt the stuff now.");
  console.log(average_bmi);
  console.log(change_bmi);
  console.log(bmi_message);
});
