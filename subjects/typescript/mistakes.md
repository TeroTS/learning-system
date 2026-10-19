# Mistakes

Earlier mistakes are preserved in `archive/pre-refresher/mistakes.md`.

- 2026-10-18 | socratic-questioner | variables-and-control-flow: predicted 5 + "2" produces numeric 7 through implicit numeric conversion | With a string operand, + performs string concatenation; the result is "52", a string.
- 2026-10-18 | socratic-questioner | variables-and-control-flow: predicted logical OR and AND always return booleans, giving true and false for 0 OR 10 and 0 AND 10 | Logical operators return operand values: OR returns the first truthy operand or the last operand; AND returns the first falsy operand or the last operand.
- 2026-10-18 | socratic-questioner | variables-and-control-flow: classified an object literal as a primitive | Objects are non-primitive; JavaScript primitive types are string, number, boolean, undefined, null, bigint and symbol.
- 2026-10-18 | socratic-questioner | variables-and-control-flow: predicted separately created empty objects are strictly equal because their types and contents match | Strict equality compares object identity, not contents; separately created objects are not strictly equal.
- 2026-10-18 | examiner | variables-and-control-flow: countAffordable returned immediately when the remaining balance reached zero, missing later affordable zero costs | Stop only at an unaffordable cost or the end of the list; a zero balance can still pay subsequent zero costs.
- 2026-10-19 | socratic-questioner | declarations-and-scope: predicted access before an inner let declaration reads the outer binding and then prints the inner value | The inner let binding shadows the outer binding throughout the function body; access before its initialization throws ReferenceError due to the temporal dead zone, so neither log prints a value.
- 2026-10-19 | socratic-questioner | declarations-and-scope: predicted access before an inner var declaration prints the outer binding | A function-scoped var binding shadows the outer binding throughout the function and is initialized to undefined before body execution; the later initializer assigns the inner string.
