# Test Results

The Manul Testing document can be found here : [ Manual Test Results](/assets/testing/integration-test.numbers).

---

## Test Strategy

The test strategy consisted of a combination of manual and automated tests.

- Parts of the appliction rely on CRUD operations to an external DB and the Garmin API, manual test cases were created to ensure isolate those tests that require internet access. It may have been done with Selenium, but keeping in mind the MVP of this iteration, it was chosen to follow a manual test strategy here.
- The main parts of automated testing focussed on python unit testing with the pytest framework. Most of the functions were isolated from Django in separate files, in order to ensure atomic unit testing of pure application logic following a principle of **design for testability**. The Django functions then simply import the tested functions using pythons `import` statement.
- For a few python helper functions, the DB access was mocked using `FactoryBoy` package
- The modules for JS were tested both manual and automatically using the JEST framework

---

## Table of Content

- [Test Results](#test-results)
  - [Test Strategy](#test-strategy)
  - [Table of Content](#table-of-content)
  - [Manual Testing](#manual-testing)
    - [Results of Authentication Tests](#results-of-authentication-tests)
    - [Results of Functionality Tests](#results-of-functionality-tests)
    - [Results of User Stories Test](#results-of-user-stories-test)
    - [Results of Other Tests](#results-of-other-tests)
    - [Results W3C HTML Validation](#results-w3c-html-validation)
    - [Results W3C CSS Validation](#results-w3c-css-validation)
    - [Results Jshint Javascript Validation](#results-jshint-javascript-validation)
    - [Results Flake8 Python Syntax Validation](#results-flake8-python-syntax-validation)
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

## Manual Testing

### Results of Authentication Tests

The authentication mechanisms of all pages of the website have been tested, including throwing of 403 erros for unauthorized acess, and the entire signup/login functionality. All tests passed.

<table>
  <tr>
    <th style='width:100%'> Verify User Stories</th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/authentication.png'  alt='Results for Authentication Tests'>
    </td>
  </tr>
</table>

### Results of Functionality Tests

All pages of the website have been tested for functionality. All tests passed.

<table>
  <tr>
    <th style='width:100%'> Verify User Stories</th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/functionality.png'  alt='Results of Functionality Tests'>
    </td>
  </tr>
</table>

### Results of User Stories Test

The user stories have been tested case-by-case. All tests passed.

<table>
  <tr>
    <th style='width:100%'> Verify User Stories</th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/user-stories-1.png'  alt='Validation User Stories screenshot'>
    </td>
  </tr>
  <tr>
    <td>
        <img src='/assets/testing/user-stories-2.png'  alt='Validation User Stories screenshot'>
    </td>
  </tr>
</table>

### Results of Other Tests

### Results W3C HTML Validation

All Pages were tested with the offical W2C HTML validator [Markup Validation Service](https://validator.w3.org/) using the option 'Validate by Direct Input', copying the rendered html code from the browser with `Right Click > View Page Source`.

All tests passed.

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
      <td style="width:70%"> <img src='/assets/testing/html-validation-profile.png'  alt='Validation Results screenshot'></td>
      <td style="width:20%"> Passed </td>
   </tr>
    <tr>
      <td style="text-align:center"> Profile</td>
      <td style="width:70%"> 
        <img src='/assets/testing/html-validation-activities-1.png'  alt='Validation Results screenshot'>
        <img src='/assets/testing/html-validation-activities-2.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%"> Passed. Regarding warnings about `Bokeh` plot: these scripts are entered by the Bokeh JS library automatically. Re-naming and messing with it seemed not advisable, nor reasonable, nor necessary. </td>
   </tr>
    <tr>
      <td style="text-align:center"> Login</td>
      <td style="width:70%"> 
        <img src='/assets/testing/html-validation-login.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%"> Passed. </td>
   </tr>
   <tr>
      <td style="text-align:center"> Signup</td>
      <td style="width:70%"> 
        <img src='/assets/testing/html-validation-signup-1.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%"> Passed (except for a `ul` element that was rendered automatically by the crispy-tailwind library inside a "small" tag. See further argumentation below.) </td>
   </tr>
    <tr>
      <td style="text-align:center"> 404 Page</td>
      <td style="width:70%"> 
        <img src='/assets/testing/html-validation-404.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%">  </td>
   </tr>
    <tr>
      <td style="text-align:center"> 403 Page</td>
      <td style="width:70%"> 
        <img src='/assets/testing/html-validation-403.png'  alt='Validation Results screenshot'>
      </td>
      <td style="width:20%">  </td>
   </tr>
</table>

### Results W3C CSS Validation

All custom written CSS passed the W2C Validator. The CSS created from the Tailwind CSS build process can be assumed to function correctly and is therefore not included in the tests.

<table style="width:90%">
  <tr>
      <th style="text-align:center"> Page</th>
      <th style="width:50%"> Output</th>
      <th style="width:10%"> Result</th>
   </tr>
   <tr>
      <td style="text-align:center"> Home</td>
      <td style="width:70%"> <img src='/assets/testing/css-validation-custom.png'  alt='Validation Results screenshot'></td>
      <td style="width:10%"> Passed </td>
   </tr>

</table>

### Results Jshint Javascript Validation

In the table below the outputs of the JSHint Validation results. No significant errors occured.

<table>
  <tr>
    <th>File</th>
    <th style='width:20%'>Result</th>
    <th> Justificaction of insignificant errors  </th>
  </tr>
  <tr>
    <td>activities.js</td>
    <td> 0 errors, 0 warnings </td>
    <td>    </td>
  </tr>
   <tr>
    <td>helper.js</td>
    <td>0 errors, 0 warnings  </td>
    <td>   </td>
  </tr>
   <tr>
    <td>helper.test.js</td>
    <td>0 errors,  0 warnings </td>
    <td>   </td>
  </tr>
   <tr>
    <td>summary.js</td>
    <td>0 errors, 2 warnings </td>
    <td> warnings regarding ES8 modules. 'Trailing comma in arguments lists' is only available in ES8 (use 'esversion: 8'). Was considered not significant   </td>
  </tr>
</table>

### Results Flake8 Python Syntax Validation

In the table below the outputs of the Flake8 Python Validation results. No significant errors occured.

<table>
  <tr>
    <th> Flake8 linter output </th>
    <th style='width:20%'>Result</th>
  </tr>
   <tr>
     <td style="width:70%"> 
        <img src='/assets/testing/flake8-validation-2.png'  alt='Validation Python Results screenshot'>
      </td>
    <td> Passed - The warnings regarding the migrations will be ignored as they were automatically generated from Django.  </td>
  </tr>
</table>

### Issues Found During Manual Testing

There were several issues found during Manual Testing that required refactoring of the code to make it pass the test.

<table style="width:90%">
    <tr>
        <th style="text-align:center;width:10%"> Test Case</th>
        <th style="width:35%"> Description </th>
        <th style="width:60%"> Errors Found  </th>
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
      <tr>
      <td style="text-align:center"> TC_22  </td>
      <td> Validate that all html files pass W3C HTML Validation Tool  </td>
      <td> 
         <ul>
            <li> In the first round, all htmx attributes of the buttons created warning of the W3C HTML validator </li>
            <li> It was tried to replace buttons with spans (and even divs as per htmx documentation), same result
            </li>
            <li> It was then decided to keep the button elements, and document the validation errors. </li>
            <li> The solution was (as found on the Project-Portfolio-4 Slack Channel, 1.April 2022, M. Bodden + Ed_B_alumn) to prepend all hx-get, hx-delete etc attribues with data-hx-get, data-hx-delete. All tests passed then.  </li>
         </ul>
           <img src='/assets/testing/errors-found/html-validation-htmx-1.png'  alt='Validation Results screenshot'>
          <img src='/assets/testing/errors-found/html-validation-htmx-2.png'  alt='Validation Results screenshot'>
          <img src='/assets/testing/errors-found/html-validation-htmx-3.png'  alt='Validation Results screenshot'>
     </td>
    </tr>
      </tr>
      <tr>
      <td style="text-align:center"> TC_22  </td>
      <td> Validate that all html files pass W3C HTML Validation Tool  </td>
      <td> 
         <ul>
            <li> In the first round, the tailwind-cripsyform library rendered a form that did not pass the W2C HTML validator </li>
            <li> Removing the label attribute on the corresponding Django form (forms.GarminForm) ensured that the crispyform library rendered and W2C passed.
            </li>
         </ul>
         <img src='/assets/testing/errors-found/html-validation-error-tailwind-crispy-forms-1.png'  alt='Validation tailwind-crispyforms'>
         <img src='/assets/testing/errors-found/html-validation-error-tailwind-crispy-forms-2.png'  alt='Validation tailwind-crispyforms'>
     </td>
    </tr>
     </tr>
      </tr>
      <tr>
        <td style="text-align:center"> TC_22  </td>
        <td> Validate that all html files pass W3C HTML Validation Tool  </td>
        <td> 
          <ul>
              <li> For the Signup page, the tailwind-cripsyform library rendered a form that did not pass the W2C HTML validator </li>
              <li> Since tailwind-crispy is still in early stages of development, there was no easy fix for this. I tried replacing the 'small' tags with 'p' tags using javascript (while the rendered page was correct, the W2C validator still complained). 
              </li>
              <li>It did not seem reasonable to create a manual form with many lines of code, only to replace the elegant one-liner <strong> forms | crispy</strong>, especially in terms of code readibility and maintainability
              </li>
              <li> In the end, this error was considered insignificant and it was decided to leave the form rendered by crispy-tailwind.
              </li>
          </ul>
          <img src='/assets/testing/html-validation-signup-1.png'  alt='Validation tailwind-crispyforms'>
          <img src='/assets/testing/html-validation-signup-3.png'  alt='Validation tailwind-crispyforms'>
          <img src='/assets/testing/html-validation-signup-2.png'  alt='Validation tailwind-crispyforms'>
      </td>
    </tr>
    <tr>
        <td style="text-align:center"> TC_25  </td>
        <td> Validate that all python files pass flake8 Validation Tool  </td>
        <td> 
          <ul>
              <li> In the first run, several issues were flagged by flake8 regaring 'Line too long' and unused variables </li>
              <li> After addressing these errors in the code, all of these issues were resolved </li>
              <li> the remaining issues raised by flake8 are concerned with files that Django created for the migrations, which will be left untouched. As a result, tests was then marked as PASSED. </li>
          </ul>
          <img src='/assets/testing/flake8-validation-1.png'  alt='Validation flake8 before refactoring'>
      </td>
    </tr>
   <tr>
        <td style="text-align:center"> TC_28  </td>
        <td>Validate website with Google Chrome Lighthouse Tools  </td>
        <td> 
          <ul>
              <li> In the first run, lighthouse flagged that several buttons on the on the activities pages did not have an `aria` label for screen readers, and scored low</li>
              <li> After adding aria-label" labels , the lighthouse accessiblity score was above 90% and the test passed </li>
          </ul>
          <img src='/assets/testing/lighthouse/lighthouse-buttons.png'  alt='Validation flake8 before refactoring'>
      </td>
    </tr>

 </table>

---

## Tests of Accessibility

### Results A11y Color Test

### Results WebAIM Accesibility Test

While the home page could be checkecd via URL in the automatic color contrast checker, that was not possible for the authenticated pages. For the pages that required authentication, only the color contrast check was done mannually for each background-to-text color pair on the page. All Tests passed.

<table>
  <tr>
    <th>
      Wave WebAim Accessibility evalulation - Home Page
    </th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/wave-webaim.png'  alt='Wave WebAim Check - Home Page'>
    </td>
  </tr>
</table>


<table>
  <tr>
    <th>  Color  </th>
    <th>  Result   </th>
  </tr>
  <tr>
    <td> <img src='/assets/testing/wave-webaim.png'  alt='Wave WebAim Check - Home Page'> </td>
    <td> <img src='/assets/testing/wave-webaim.png'  alt='Wave WebAim Check - Home Page'> </td>
  </tr>
</table>




### Results Chrome Lighthouse

All pages were tested with Google lighthouse using the `chrome-debug` browser as described in this document, using Option 4 of the Lighthouse documentation for testing authenticated pages [Running Lighthouse on Authenticated Pages](https://github.com/GoogleChrome/lighthouse/blob/main/docs/authenticated-pages.md), after globablly installing `lighthouse` with `node`. All Tests passed.

<table>
  <tr>
    <th>
      Google Lighthouse - Activities Page (Authenticated)
    </th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/lighthouse/lighthouse.png'  alt='Lighthouse Scores - Activities Page'>
    </td>
  </tr>
</table>

<table>
  <tr>
    <th>
      Google Lighthouse - Profile Page (Authenticated)
    </th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/lighthouse/lighthouse-profile.png'  alt='Lighthouse Scores - Profile Page'>
    </td>
  </tr>
</table>

<table>
  <tr>
    <th>
      Google Lighthouse - Home Page
    </th>
  </tr>
  <tr>
    <td>
      <img src='/assets/testing/lighthouse/lighthouse-home.png'  alt='Lighthouse Scores - Home Page'>
    </td>
  </tr>
</table>

---

## Tests for Compatibility

---

## Automated Testing

### Results of testing framework for Javascript (Jest)

### Results of testing framework for Python (Pytest)

#### Coverage Report

---
