# Test Results

The Integration Testing document can be found here : [ Integration Test Results](/assets/testing/integration-test.numbers).

---

- [Test Results](#test-results)
  - [Test Strategy](#test-strategy)
  - [Integration Tests (Manual Testing)](#integration-tests-manual-testing)
    - [Results of Syntax Validation with PEP8](#results-of-syntax-validation-with-pep8)
    - [Results of User Stories Test](#results-of-user-stories-test)
    - [Results of Functionality Tests](#results-of-functionality-tests)
    - [Results of Other Tests](#results-of-other-tests)
    - [Results W3C HTML Validation](#results-w3c-html-validation)
    - [Results W3C CSS Validation](#results-w3c-css-validation)
    - [Results Jshint Javascript Validation](#results-jshint-javascript-validation)
    - [Issues Found During Manual Testing](#issues-found-during-manual-testing)
  - [Tests of Accessibility](#tests-of-accessibility)
    - [Results A11y Color Test](#results-a11y-color-test)
    - [Results WebAIM Accesibility Test](#results-webaim-accesibility-test)
    - [Results Chrome Lighthouse](#results-chrome-lighthouse)
  - [Tests for Compatibility](#tests-for-compatibility)
  - [Automated Testing](#automated-testing)
    - [Results of testing framework for Javascript (Jest)](#results-of-testing-framework-for-javascript-jest)
    - [Results of testing framework for Python (Pytest)](#results-of-testing-framework-for-python-pytest)
      - [Coverage Report](#coverage-report)

---

## Test Strategy

- Integration Tests
- Automated Tests
  - Coverage Reports
- Test-driven Development
  - Testing View Functions (Django)
  - Testing Models with Factory Boy (Pytest)
  - Tests for Javascript

---

## Integration Tests (Manual Testing)

<table>

### Results of Syntax Validation with PEP8

### Results of User Stories Test

### Results of Functionality Tests

### Results of Other Tests

### Results W3C HTML Validation

### Results W3C CSS Validation

### Results Jshint Javascript Validation

### Issues Found During Manual Testing

There were several issues found during Manual Testing that required refactoring of the code to make it pass the test.

<table style="width:90%">
    <tr>
        <th style="text-align:center"> Test Case</th>
        <th style="width:45%"> Description </th>
        <th style="width:45%"> Errors Found  </th>
    </tr>
    <tr>
      <td style="text-align:center"> TC-03 (second pass) </td>
      <td> Ensure that all URLs on the Dashboard Page can only be accessed by authenticated users. For unauthenticated users it should raise 403 error.  </td>
      <td> 
        <ul>
          <li> In the first round, a 500 server error was raised. A view did not check if a user was authenticated, and tried to find records in the DB for the AnonymousUser </li>
          <li> After adding appropriate checks to the view function, the 403 error was raised correctly, and the test passed </li>
        </ul>
      </td>
    </tr>
 </table>

---

## Tests of Accessibility

### Results A11y Color Test

### Results WebAIM Accesibility Test

### Results Chrome Lighthouse

---

## Tests for Compatibility

---

## Automated Testing

### Results of testing framework for Javascript (Jest)

### Results of testing framework for Python (Pytest)

#### Coverage Report

---
