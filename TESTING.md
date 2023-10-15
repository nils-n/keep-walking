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

The only issue found during HTML validation was that [htmx](https://htmx.org/attributes/hx-get/) attributes are not yet allowed by the W3C HTML validator. I tried to replace the `button` element with a`span` and a `div` (as per original documentation of `htmx`) but same result. I then decided to use a `button` element for all the elements using `hx-get`, `hx-delete`, and leave the errors documented here.

Other than the htmx-attributes , all tests passed.

<table style="width:90%">
  <tr>
      <th style="text-align:center"> Page</th>
      <th style="width:50%"> Output</th>
      <th style="width:10%"> Result</th>
   </tr>
   <tr>
      <td style="text-align:center"> Home</td>
      <td style="width:70%"> <img src='/assets/testing/html-validation-home.png'  alt='Validation Results screenshot'></td>
      <td style="width:10%"> Passed </td>
   </tr>
    <tr>
      <td style="text-align:center"> Profile</td>
      <td style="width:70%"> 
          <img src='/assets/testing/html-validation-htmx-1.png'  alt='Validation Results screenshot'>
          <img src='/assets/testing/html-validation-htmx-2.png'  alt='Validation Results screenshot'>
          <img src='/assets/testing/html-validation-htmx-3.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%"> Passed (with expected fail for htmx elements). Explanation see above. </td>
   </tr>
</table>

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
      <td style="text-align:center"> TC_03 </td>
      <td> Ensure that all URLs on the Dashboard Page can only be accessed by authenticated users. For unauthenticated users it should raise 403 error.  </td>
      <td> 
         <ul>
            <li> In the first round, a 500 server error was raised. A view did not check if a user was authenticated, and tried to find records in the DB for the AnonymousUser </li>
            <li> After adding appropriate checks to the view function, the 403 error was raised correctly, and the test passed </li>
         </ul>
     </td>
     </tr>
     <tr>
      <td style="text-align:center"> TC_19  </td>
      <td> User Story 7 : As a signed in user I can load my health stats from my Garmin watch so that (over time) I can track my exact step count and my weight measurements from the Garmin App </td>
      <td> 
         <ul>
            <li> In the first round, it was noted that there was no feedback (in form of a toast message) telling the user that the synchronisation was successful </li>
            <li> After refactoring the corresponding view function, the correct toasts appeared, and test passed
            </li>
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
