
Concepts
========

.. warning:: This section is work in progress and there will be areas that are lacking.

Motivation
----------

    "Have a look at this piece of code that I'm writing--I'm sure it has been written before.
    I wouldn't be surprised to find it verbatim somewhere on GitHub." - `@kr1 <https://github.com/kr1>`_

Every piece of functionality in a software project
requires code that lies somewhere in the wide reusability spectrum that goes
form extremely custom and strongly tied to the specific implementation
to completely generic and highly reusable.

On the *custom* side of the spectrum there is all the code that defines the
features of the software and all the choices of its implementation. That one is code that need
to be written.

On the other hand a seasoned software developer is trained to spot
pieces of functionality that lie far enough on the *generic* side of the range
that with high probability a library already implements it
**and documents it well enough to be discovered with an internet search**.

In between the two extremes there is a huge gray area populated by pieces of functionality
that are not *generic* enough to obviously deserve a place in a library, but are
*common* enough that must have been already implemented by someone else for their
software. This kind of code is doomed to be re-implemented again and again
for the simple reason that **there is no way to search code by functionality**...

Or is it?


Test-driven code search
-----------------------

When developing new functionalities developers spend significant efforts searching for
code to reuse, mainly via keyword-based searches, e.g. on StackOverflow and Google.
Keyword-based search is quite effective in finding code that is explicitly designed and
documented to be reused, e.g. libraries and frameworks,
but typically fails to identify reusable functions and classes in the large corpus of
auxiliary code of software projects.

TDR aims to address the limits of keyword-based search with test-driven code search
that focuses instead on code behaviour and semantics.
Developing a new feature in TDR starts with the developer writing the tests
that will validate candidate implementations of the desired functionality.
Before writing any functional code the tests are run against all functions
and classes of all available projects.
Any code passing the tests is presented to the developer
as a candidate implementation for the target feature.

pytest-nodev is a pytest plugin that enables *test-driven code search* and
consequently a software development strategy called
*test-driven reuse* or TDR that we call *nodev*,
that is an extension of the well known *test-driven development* or TDD.

The idea is that once the developer has written the tests that define the behaviour of a new
function to a degree sufficient to validate the implementation they are going to write
it is good enough to validate
any implementation. Running the tests on a large set of functions may result in a *passed*, that is
a function that already implements their feature.

Due to its nature the approach is better suited for discovering smaller functions
with a generic signature.


Tests validation
----------------

Another use for pytest-nodev is, with a bit of additional work, to validate a project test suite.
If a test passes with an unexpected object there are two possibilities,
either the test is not strict enough and allows for false positives and needs to be updated,
or the *passed* is actually a function you could use instead of your implementation.


Keywords:

 * Source code *search by feature*, *search by functionality*, *search by specification* or *nodev*
 * *Feature-specification test* and test suite or *Requirement-specification test*
 * *Test-driven reuse* or *test-driven code search* or *test-driven source code search*


Bibliography
------------

- "CodeGenie: a tool for test-driven source code search", O.A. Lazzarini Lemos *et al*,
  Companion to the 22nd ACM SIGPLAN conference on Object-oriented programming systems and applications companion,
  917--918, **2007**, ACM, http://dx.doi.org/10.1145/1297846.1297944

- "Code conjurer: Pulling reusable software out of thin air", O. Hummel *et al*,
  IEEE Software, (25) 5 45-52, **2008**, IEEE, http://dx.doi.org/10.1109/MS.2008.110 ---
  `PDF <http://cosc612.googlecode.com/svn/Research%20Paper/Code%20Conjurer.pdf>`__

- "Finding Source Code on the Web for Remix and Reuse", S.E. Sim *et al*, 251, **2013** ---
  `PDF <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.308.2645&rep=rep1&type=pdf>`__

- "Test-Driven Reuse: Improving the Selection of Semantically Relevant Code", M. Nurolahzade,
  Ph.D. thesis, **2014**, UNIVERSITY OF CALGARY ---
  `PDF <http://lsmr.org/docs/nurolahzade_phd_2014.pdf>`__
