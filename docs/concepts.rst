
Concepts
========

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

On the other hand seasoned software developers are trained to spot
pieces of functionality that lie far enough on the *generic* side of the range
that with high probability are already implemented in a **librariy** or a **framework**
and that are documented well enough to be discovered with a
**keyword-based search**, e.g. on StackOverflow and Google.

In between the two extremes there is a huge gray area populated by pieces of functionality
that are not *generic* enough to obviously deserve a place in a library, but are
*common* enough that must have been already implemented by someone else for their
software. This kind of code is doomed to be re-implemented again and again
for the simple reason that **there is no way to search code by functionality**...

Or is it?


Test-driven code search
-----------------------

To address the limits of keyword-based search *test-driven code search*
focuses on code behaviour and semantics instead.

The **search query** is a test function that is executed once for every
candidate class or function available to the **search engine**
and the **search result** is the list of candidates that pass the test.

Due to its nature the approach is better suited for discovering smaller functions
with a generic signature.

*pytest-nodev* is a pytest plugin that enables *test-driven code search* for Python.


Test-driven code reuse
----------------------

*Test-driven reuse* (TDR) is an extension of the well known *test-driven development* (TDD)
development practice.

Developing a new feature in TDR starts with the developer writing the tests
that will validate the correct implementation of the desired functionality.

Before writing any functional code the tests are run against all functions
and classes of all available projects.

Any code passing the tests is presented to the developer
as a candidate implementation for the target feature:


- if nothing passes the tests the developer need to implement the feature and TDR reduces to TDD
- if any code passes the tests the developer can:

  - **import**: accept code as a dependency and use the class / function directly
  - **fork**: copy the code and the related tests into their project
  - **study**: use the code and the related tests as guidelines for their implementation,
    in particular identifyng corner cases and optimizations


Unit tests validation
---------------------

An independent use case for test-driven code search is unit tests validation.
If a test passes with an unexpected object there are two possibilities,
either the test is not strict enough and allows for false positives and needs to be updated,
or the *PASSED* is actually a function you could use instead of your implementation.


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
