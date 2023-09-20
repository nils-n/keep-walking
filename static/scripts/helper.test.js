const helpers = require("./helper");
const sum = helpers.sum;
const getBMIstatus = helpers.getBMIstatus;

test("a BMI within a healthy range should returns correct summary", () => {
  expect(getBMIstatus(16)).toBe("too low");
  expect(getBMIstatus(24)).toBe("just right");
  expect(getBMIstatus(24)).toBe("just right");
  expect(getBMIstatus(26)).toBe("too high");
  expect(getBMIstatus(30)).toBe("too high");
});
