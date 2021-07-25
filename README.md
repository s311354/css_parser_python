
## Anatomy of a CSS ruleset

The whole structure is called a ruleset. (The term ruleset is often referred to as just rule.) Note the names of the individual parts:

Selector
This is the HTML element name at the start of the ruleset. It defines the element(s) to be styled (in this example, <p> elements). To style a different element, change the selector.

Declaration
This is a single rule like color: red;. It specifies which of the element's properties you want to style.

Properties
These are ways in which you can style an HTML element. (In this example, color is a property of the <p> elements.) In CSS, you choose which properties you want to affect in the rule.

Property value
To the right of the property—after the colon—there is the property value. This chooses one out of many possible appearances for a given property. (For example, there are many color values in addition to red.)
Note the other important parts of the syntax:
* Apart from the selector, each ruleset must be wrapped in curly braces. ({})
* Within each declaration, you must use a colon (:) to separate the property from its value or values.
* Within each ruleset, you must use a semicolon (;) to separate each declaration from the next one.

## Different types of selectors

There are many different types of selectors. The examples above use element selectors, which select all elements of a given type. But we can make more specific selections as well. Here are some of the more common types of selectors:

## Reference ##
[1] [CSS basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/CSS_basics)

