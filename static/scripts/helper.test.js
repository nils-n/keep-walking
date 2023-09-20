const helpers = require("./helper");
const sum = helpers.sum;
const getBMIstatus = helpers.getBMIstatus;

test("a BMI within a healthy range should returns correct summary", () => {
  expect(getBMIstatus(20)).toBe("just right");
});
