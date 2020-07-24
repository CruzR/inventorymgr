=====================
Security Requirements
=====================

This document lays out the security requirements for the project.

It is inspired by the OWASP Application Security Verification Standard (ASVS).
For now, the goal is to meet all ASVS level 1 requirements,
but in the long term, most level 2 requirements should be evaluated aswell.

Where possible, this document also links to other standards that may influence
our thinking, and tries to discuss concrete solutions.


V1: Architecture, Design and Threat Modeling
============================================

None of the requirements listed in this section are required for Level 1
compliance, so implementation is deferred until meeting Level 2 requirements
becomes a goal.


V2: Authentication
==================

Besides ASVS, NIST 800-63b is also a relevant standard.


V2.1 Password Security
----------------------

Password security requirements can roughly be split into three groups:

- Requirements that limit the transforms that may be performed on a password
- Guidelines for what constitutes a valid password
- Guidelines for UI related to passwords

In order to satisfy the requirements from the first two groups, but stil stay
flexible, the following architecture seems reasonable:

1. Apply a configurable list of transformation steps.
2. Run a configurable list of validation functions. If any function flags the
  password as invalid, reject the password.

If deemed necessary, select steps could happen out of process with minimal
privileges to avoid security or stability issues.

  2.1.1: Verify that user set passwords are at least 12 characters in length.

This implies one of the password validation filters should reject any password
shorter than 12 characters.

.. code:

  def validate_min_length(passwd):
      return len(passwd) >= 12

..

  2.1.2: Verify that passwords 64 characters or longer are permitted.

This implies that neither the web forms nor the password validation should
limit the password length to less than 64 characters. Modern password hashing
algorithms should not have an issue with passwords of arbitrary length.

No length limit at all would of course be ideal, but in order to prevent DoS
attacks, we should put a limit on the allowed request size at the HTTP server
level, which would implicitly also limit the password length.

But as long as that request size limit is sufficiently high - say, 64K - this
should not pose usability issues.

  2.1.3: Verify that passwords can contain spaces and truncation is not
  performed. Consecutive multiple spaces MAY optionally be coalesced.

Coalescing multiple consecutive spaces is probably a good idea from a user
experience standpoint, even though it slightly reduces entropy.

Other than that, modern password hashing functions should be using the whole
password string, so we are probably good regarding truncation.

  2.1.4: Verify that Unicode characters are permitted in passwords. A single
  Unicode code point is considered a character,so 12 emoji or 64 kanji
  characters should be valid and permitted.

Password hashing functions should work on arbitrary byte strings, so we just
need to ensure to encode to UTF-8.

  2.1.5: Verify users can change their password.

This one is pretty obvious.

  2.1.6: Verify that password change functionality requires the user's current
  and new password.

This does raise questions of whether resetting lost passwords using another
authentication factor is permitted, but that should probably be treated
separately from a normal password change.

It is also unclear whether the change should be rejected if the old and new
passwords are identical. Some thought should be put into the effects on UX.

  2.1.7: Verify that passwords submitted during account registration, login,
  and password change are checked against of breached passwords either locally
  (such as the top 1,000 or 10,000 most common passwords which match the system's
  password policy) or using an external API. If using an API a zero knowledge
  proof or other mechanism should be used to ensure that the plain text password
  is not sent or used in verifying the breach status of the password. If the
  password is breached, the application must require the user to set a new
  non-breached password.

HaveIBeenPwned provides an HTTP API for querying whether a password has been
compromised in one of the breaches in its huge breach database.
The API takes the first couple of hex digits of the password's SHA1 hashsum,
and returns all the suffixes in its DB that match that prefix.

However, at least one paper has been published that demonstrates that this
might be enough to significantly increase the probability of guessing a
matching username and cleartext password from a dump of breached credentials,
so we need to evaluate whether this has a negative net effect on security.

Alternatively, the database of password hashes and breach counts is also
available for download from HIBP, so we could use a key-value store to check
this without a network request to external services.

  2.1.8: Verify that a password strength meter is provided to help users set
  a stronger password.

There is a JS library for this: [zxcvbn](https://github.com/dropbox/zxcvbn).

However, it is quite large (400kB minified), written in CoffeeScript, optimized
for English and has not been updated since 2017.  We need to investigate
whether using it is a good decision.

For display, we probably should not use the HTML `<meter>` element, because it
cannot be styled.

The server should also enforce the same rules. Fortunately, there also is a
Python port of zxcvbn.

  2.1.9: Verify that there are no password composition rules limiting the type
  of characters permitted.

It is unclear whether this allows doing Unicode normalization, which would be
desirable from an UX standpoint.

It probably means that using PRECIS, the IETF standard for _Preparation,
Enforcement and Comparison of Internationalized Strings Representing Usernames
and Passwords_ as specified in [RFC 8265](https://tools.ietf.org/html/rfc8265),
is not possible for passwords, because it prohibits certain character classes,
namely Old Hangul Jamo code points, Control code points and Precis Ignorable
code points, by reference to the PRECIS `FreeformClass` specified in
[RFC 8264, Section 4.3](https://tools.ietf.org/html/rfc8264#section-4.3).

  2.1.10 Verify that there are no periodic credential rotation or password
  history requirements.

That is easy to verify by simply not building such a "feature".

  2.1.11 Verify that "paste" functionality, browser password helpers, and
  external password managers are permitted.

This should be the default behavior of HTML5 `password` inputs. We can go even
further and provide hints for browsers / password manager browser addons for
which inputs are intended for new passwords on signup and password change
forms.

  2.1.12 Verify that the user choose to either temporarily view the entire
  masked password, or temporarily view the last typed character of the password
  on platforms that do not have this as native functionality.

At least Firefox and Chrome do not provide this functionality on desktop, so
this needs to be implemented in JavaScript.

Some user research is required to determine whether it is better to replace
the native functionality on all platforms, or whether to only do this when
there is no native support.