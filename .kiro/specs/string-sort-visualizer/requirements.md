# Requirements Document

## Introduction

A Streamlit web application that enables users to sort collections of strings using three classic sorting algorithms — Bubble Sort, Selection Sort, and Quick Sort. Users can either enter strings manually or pick from a predefined word list. After triggering a sort, the application displays the sorted output and the number of comparison steps each algorithm required, allowing users to compare algorithm efficiency at a glance.

## Glossary

- **Application**: The Streamlit-based string sorting web application.
- **User**: A person interacting with the Application through a web browser.
- **String_Input**: A collection of strings provided by the User, either typed manually or selected from the Predefined_Word_List.
- **Predefined_Word_List**: A fixed set of example strings bundled with the Application that a User can select from.
- **Sorting_Algorithm**: One of the three implemented algorithms: Bubble Sort, Selection Sort, or Quick Sort.
- **Sort_Result**: The sorted list of strings produced by a Sorting_Algorithm.
- **Step_Count**: The number of comparison operations performed by a Sorting_Algorithm to produce a Sort_Result.
- **Accuracy_Check**: A verification that the Sort_Result is correctly ordered in ascending lexicographic order.
- **Sort_Button**: The UI control that triggers sorting execution in the backend.

---

## Requirements

### Requirement 1: String Input — Manual Entry

**User Story:** As a User, I want to type strings directly into the Application, so that I can sort any custom set of words I choose.

#### Acceptance Criteria

1. THE Application SHALL provide a text input area where the User can enter one string per line.
2. WHEN the User activates the Sort_Button, IF the text input area contains no lines with non-whitespace characters after trimming, THEN THE Application SHALL display a validation message indicating that at least one string is required.
3. WHEN the User enters duplicate strings (case-sensitive, after trimming), THE Application SHALL preserve all duplicates in the String_Input without deduplication.
4. THE Application SHALL trim leading and trailing whitespace from each entered string before processing.
5. THE Application SHALL accept a maximum of 1,000 strings per input, where each individual string is at most 500 characters in length.

---

### Requirement 2: String Input — Predefined Word List

**User Story:** As a User, I want to pick strings from a predefined list, so that I can quickly try out the sorting algorithms without typing.

#### Acceptance Criteria

1. THE Application SHALL display a selection widget containing the Predefined_Word_List.
2. WHEN the User selects one or more entries from the Predefined_Word_List, THE Application SHALL populate the String_Input with the selected strings, replacing any previously entered manual input.
3. THE Predefined_Word_List SHALL contain at least 20 example strings, where individual strings range from 1 to 20 characters in length and the list includes strings composed of lowercase letters, uppercase letters, digits, and mixed-character combinations.
4. WHEN the User selects strings from the Predefined_Word_List and also has manually entered strings, THE Application SHALL use the Predefined_Word_List selection as the active String_Input, replacing the manual entry; IF the User subsequently deselects all entries from the Predefined_Word_List, THEN THE Application SHALL restore the String_Input to the previously entered manual content.
5. THE Application SHALL allow the User to select up to 50 entries simultaneously from the Predefined_Word_List.

---

### Requirement 3: Sorting Execution

**User Story:** As a User, I want to trigger sorting by clicking a button, so that I have explicit control over when the computation runs.

#### Acceptance Criteria

1. THE Application SHALL display a Sort_Button that the User can activate to start sorting.
2. WHEN the User activates the Sort_Button, THE Application SHALL execute all three Sorting_Algorithms (Bubble Sort, Selection Sort, Quick Sort) against the String_Input.
3. WHEN the User activates the Sort_Button, IF the String_Input contains between 1 and 1,000 non-empty strings, THEN THE Application SHALL display Sort_Results for all three Sorting_Algorithms within 5 seconds.
4. WHEN the User activates the Sort_Button, IF the String_Input is empty, THEN THE Application SHALL display a validation message indicating that input is required and SHALL NOT execute any Sorting_Algorithm.
5. WHILE a Sorting_Algorithm execution is in progress, THE Application SHALL disable the Sort_Button so that the User cannot trigger a new sort until the current execution completes.

---

### Requirement 4: Bubble Sort Algorithm

**User Story:** As a User, I want the Application to sort strings with Bubble Sort, so that I can see its step count compared to other algorithms.

#### Acceptance Criteria

1. WHEN Bubble Sort is executed on a String_Input, THE Bubble_Sort_Algorithm SHALL produce a Sort_Result sorted in ascending lexicographic order using case-sensitive comparison, where uppercase letters precede lowercase letters for the same character.
2. WHEN Bubble Sort is executed, THE Bubble_Sort_Algorithm SHALL record a Step_Count equal to the total number of pairwise string comparisons performed across all passes, including comparisons that do not result in a swap.
3. WHEN Bubble Sort is executed on an already-sorted String_Input, THE Bubble_Sort_Algorithm SHALL produce a Sort_Result identical to the String_Input with a Step_Count greater than or equal to the number of adjacent pairs in the String_Input.
4. WHEN Bubble Sort is executed on a single-element String_Input, THE Bubble_Sort_Algorithm SHALL produce a Sort_Result identical to the String_Input with a Step_Count of 0.
5. WHEN Bubble Sort is executed on an empty String_Input, THE Bubble_Sort_Algorithm SHALL produce an empty Sort_Result with a Step_Count of 0.

---

### Requirement 5: Selection Sort Algorithm

**User Story:** As a User, I want the Application to sort strings with Selection Sort, so that I can compare its efficiency against other algorithms.

#### Acceptance Criteria

1. WHEN Selection Sort is executed on a String_Input, THE Selection_Sort_Algorithm SHALL produce a Sort_Result in which every adjacent pair of strings satisfies ascending lexicographic order.
2. WHEN Selection Sort is executed, THE Selection_Sort_Algorithm SHALL record a Step_Count incremented by exactly 1 for each individual pairwise string comparison performed, including comparisons that do not result in a swap.
3. WHEN Selection Sort is executed on a String_Input in which every adjacent pair is already in ascending lexicographic order, THE Selection_Sort_Algorithm SHALL produce a Sort_Result identical to the String_Input.
4. WHEN Selection Sort is executed on a single-element String_Input, THE Selection_Sort_Algorithm SHALL produce a Sort_Result identical to the String_Input with a Step_Count of 0.
5. WHEN Selection Sort is executed on an empty String_Input, THE Selection_Sort_Algorithm SHALL produce an empty Sort_Result with a Step_Count of 0.
6. WHEN Selection Sort is executed on a String_Input containing duplicate strings, THE Selection_Sort_Algorithm SHALL preserve all duplicate strings in the Sort_Result.

---

### Requirement 6: Quick Sort Algorithm

**User Story:** As a User, I want the Application to sort strings with Quick Sort, so that I can observe its typically lower step count on larger inputs.

#### Acceptance Criteria

1. WHEN Quick Sort is executed on a String_Input, THE Quick_Sort_Algorithm SHALL produce a Sort_Result sorted in ascending case-insensitive lexicographic order, with case-sensitive tie-breaking for strings that differ only in case.
2. WHEN Quick Sort is executed, THE Quick_Sort_Algorithm SHALL record a Step_Count equal to the total number of pairwise string comparisons performed across all partitioning operations, including pivot comparisons.
3. WHEN Quick Sort is executed on an already-sorted String_Input of n elements, THE Quick_Sort_Algorithm SHALL produce a Sort_Result sorted in ascending lexicographic order with a Step_Count of at most n×(n−1)/2.
4. WHEN Quick Sort is executed on a single-element String_Input, THE Quick_Sort_Algorithm SHALL produce a Sort_Result identical to the String_Input with a Step_Count of 0.
5. WHEN Quick Sort is executed on an empty String_Input, THE Quick_Sort_Algorithm SHALL produce an empty Sort_Result with a Step_Count of 0.

---

### Requirement 7: Accuracy Verification

**User Story:** As a User, I want the Application to verify that each Sort_Result is correct, so that I can trust the output of each algorithm.

#### Acceptance Criteria

1. WHEN any Sorting_Algorithm completes execution, THE Accuracy_Check SHALL verify that the Sort_Result matches the output of Python's built-in `sorted()` function applied to the same String_Input.
2. WHEN the Accuracy_Check passes, THE Application SHALL display a success indicator next to that algorithm's result confirming the Sort_Result is correct.
3. IF the Accuracy_Check fails for any Sorting_Algorithm, THEN THE Application SHALL display an error indicator next to that algorithm's result identifying it as incorrect.
4. THE Accuracy_Check SHALL compare the Sort_Result against Python's built-in `sorted()` output for the same String_Input to determine correctness.

---

### Requirement 8: Results Display

**User Story:** As a User, I want to see the sorted output and step count for each algorithm side by side, so that I can easily compare their performance.

#### Acceptance Criteria

1. WHEN the User submits input and all three Sorting_Algorithms complete sorting, THE Application SHALL display the Sort_Result and Step_Count for each Sorting_Algorithm.
2. WHEN the User submits input and all three Sorting_Algorithms complete sorting, THE Application SHALL present each Sorting_Algorithm's results in a separate section labelled with the Sorting_Algorithm's name, arranged side by side in a single view.
3. WHEN the User submits input and all three Sorting_Algorithms complete sorting, THE Application SHALL display each Sorting_Algorithm's Step_Count as a non-negative integer accompanied by a descriptive label identifying what the count represents.
4. WHEN the User submits input and all three Sorting_Algorithms complete sorting, THE Application SHALL display each Sorting_Algorithm's Sort_Result as an ordered list of strings.
5. WHEN the User submits input and all three Sorting_Algorithms complete sorting, THE Application SHALL display a summary table showing all three Sorting_Algorithm names, their Step_Counts, and whether each Sort_Result matches the expected ascending lexicographic order of the input strings.
6. IF Sort_Results are not yet available, THEN THE Application SHALL display the results area in an empty state with no Sort_Result or Step_Count shown.
