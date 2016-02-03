
Test-Driven no-Development
--------------------------

Short story of an epiphany
..........................

A couple of years ago my colleague @kr1 was silently coding when he erupted:
"Man, I can't believe I need to write something like this."

"I know [redacted JS framework name] is total crap.
I shouldn't have accepted to use it, I'm sorry."
I replied without turning.

"No, it's not that.
Have a look at this piece of code that I'm writing...
I'm sure it has been written before.
Probably verbatim. Probably dozens of times already."
His tone was unusually excited.

I turned and looked at his monitor. "Well, sure a lot of people need to do [some common task]."

"Exactly. It's a common task, but not common enough to be found in a library as is."
He remained silent for a few seconds.
"You see, sometimes I feel like we developers spend most of our time re-implementing code
that has already been written somewhere, we just don't know where."

"I see your point...
Let's hope no one builds a search engine for code then.
Or we would be out of business in no time! Ah, ah!"

"That is precisely the point: there's no way to search code by features."

We turned back to our screens, but something had clicked in my mind.

"You can write a test." I said after a few minutes.
And that was my time to be unusually excited.

"What for?"

"To search code by features.
You write a test suite that asserts the features you want from a piece of code.
Then you run your tests on all source code on the internet and
if something passes the test suite it's the piece of code with the features you were looking for."

"Interesting."

"It's like Test-Driven Development, but without the development thing."
I said.
"And since you are going to write the tests anyway,
searching this way it's quite cheap, it doesn't require much additional effort."

"Running a test on, say, all the code on github it's not going to be easy, thou.
You need a lot of resources."

"But it's just processing time... Ah, ah, I sense we have some start-up material in our hands."