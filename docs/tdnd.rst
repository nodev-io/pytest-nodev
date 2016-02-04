
Test-Driven no-Development
--------------------------

Short story of an epiphany
..........................

A couple of years ago my colleague `@kr1`_ was silently coding when he erupted:
"Man! I can't believe I need to write something like this."

"I know [redacted JS framework name] is total crap.
I shouldn't have accepted to use it, I'm sorry."
I replied without turning.

"No, it's not that.
Have a look at this piece of code that I'm writing --
I'm sure it has been written before. Possibly dozens of times already.
I wouldn't be surprised to find it verbatim somewhere on GitHub."
His tone was unusually excited.

I turned and looked at his monitor. "Well, sure a lot of people need to do [some common task]."

"Exactly. It's a common task, but not common enough to be found in a library as is."
He remained silent for a few seconds.
"You see, sometimes I feel like we developers spend most of our time re-implementing code
that has already been written somewhere, we just don't know where."

"I see your point...
Let's hope no one builds a search engine for code then.
Or we would be out of business in no time! Ah, ah!"

"That is precisely the point: there's no way to search code by features.
I remember reading a wild proposal about something like that
by `Joe Armstrong on the erlang mailing list`_."

We turned back to our screens, but something had clicked in my mind.

"You could write a test." I said after a while.
And that was my time to be unusually excited.

"What for?"

"To search code by features.
You write a test suite that asserts the features you want from a piece of code.
Then you run your tests on all source code that you can find on the internet and
if something passes the tests it's the piece of code you were looking for."

"That's interesting."

"It's like Test-Driven Development, but without the development thing."
I said.
"And since you are going to write the tests anyway,
searching for an implementation this way it's quite cheap,
it doesn't require much additional effort."

"Well, running a test on, say, all the code on GitHub it's not going to be easy, thou.
You need a lot of resources."

"Yes, but that it's just dirty cheap CPU time --
We might have some kind of start-up material in our hands."

.. _`@kr1`: https://github.com/kr1
.. _`Joe Armstrong on the erlang mailing list`: http://erlang.org/pipermail/erlang-questions/2011-May/058768.html
